#!/usr/bin/env python3
"""Validate Markdown links, agent paths, schemas, and document controls."""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from json import JSONDecodeError, load as json_load, loads as json_loads
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_POLICY_FILE = "AGENTS.md"
ACTIVE_AGENT_DIRECTORY: str | None = "agents/templates"
SCHEMA_LOCATIONS = ("schemas",)
REQUIRED_METADATA = (
    "schema_version",
    "type",
    "template_id",
    "document_version",
    "last_edited",
)
TEMPLATE_GLOBS = ("**/*.template.md", ".github/PULL_REQUEST_TEMPLATE.md")
DOCUMENT_CONTROL_INCLUDE = ("**/*.md",)
DOCUMENT_CONTROL_EXCLUDE: tuple[str, ...] = ()
ENFORCE_AGENT_TEMPLATE_TYPES = True
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
FENCE = re.compile(r"^\s*(```|~~~)")
HIDDEN_AGENT_REFERENCE = re.compile(r"\.agents/")
PRIVATE_PATH_PATTERNS = (HIDDEN_AGENT_REFERENCE,)
DOUBLED_AGENT_SEPARATOR = re.compile(r"(?:^|[^.])agents//|\.agents//")

APPROVED_HIDDEN_AGENT_REFERENCES = {
    "ADOPTION.md": (
        re.compile(r"`agents/`, `\.agents/`, or another governed path"),
        re.compile(r"relevant `agents/`, `\.agents/`,"),
        re.compile(r"-g '\.agents/\*\*'"),
        re.compile(r"`\.agents/` directory is not inherently stale or defective"),
        re.compile(r"agents/, \.agents/, and \.claude/"),
    ),
    "README.md": (
        re.compile(r"intentional `\.agents/` discussion"),
    ),
}

REQUIRED_SCAFFOLD_PATHS = (
    "AGENTS.md",
    "AGENTS.template.md",
    "VERSIONING.template.md",
    "schemas/README.md",
    "schemas/v1/README.md",
    "schemas/v1/INTRODUCED.md",
    "schemas/v1/document-control.md",
    "schemas/v1/template-metadata.md",
    "schemas/v1/schema-contract.template.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "agents/README.md",
    "agents/templates/schema-version-steward.template.md",
)

SCHEMA_DIRECTORY = re.compile(r"^v([1-9][0-9]*)$")
PLAIN_INTEGER = re.compile(r"[-+]?(?:0|[1-9][0-9]*)$")
PLAIN_FLOAT = re.compile(
    r"[-+]?(?:(?:0|[1-9][0-9]*)\.[0-9]+|(?:0|[1-9][0-9]*)[eE][-+]?[0-9]+)$"
)
TEMPLATE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DOCUMENT_VERSION = re.compile(r"^[0-9]+\.[0-9]+$")
ISO_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
ALLOWED_TEMPLATE_TYPES = {
    "agent_contract",
    "versioning_policy",
    "agent_role",
    "schema_contract",
    "pull_request",
}
EXPECTED_TEMPLATE_TYPES = {
    "AGENTS.template.md": "agent_contract",
    "VERSIONING.template.md": "versioning_policy",
    ".github/PULL_REQUEST_TEMPLATE.md": "pull_request",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        help="JSON configuration for a downstream repository",
    )
    return parser.parse_args()


def _string_list(config: dict[str, object], key: str, default: tuple[str, ...]) -> tuple[str, ...]:
    value = config.get(key, list(default))
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be an array of strings")
    return tuple(value)


def apply_configuration(config_path: Path | None) -> None:
    """Apply optional downstream layout and policy settings."""
    if config_path is None:
        return

    resolved = config_path.resolve()
    try:
        with resolved.open(encoding="utf-8") as handle:
            config = json_load(handle)
    except (OSError, JSONDecodeError) as exc:
        raise ValueError(f"cannot read configuration {config_path}: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError("configuration root must be a JSON object")

    global ROOT
    global CANONICAL_POLICY_FILE, ACTIVE_AGENT_DIRECTORY, SCHEMA_LOCATIONS
    global REQUIRED_METADATA, TEMPLATE_GLOBS
    global DOCUMENT_CONTROL_INCLUDE, DOCUMENT_CONTROL_EXCLUDE
    global ENFORCE_AGENT_TEMPLATE_TYPES, PRIVATE_PATH_PATTERNS
    global APPROVED_HIDDEN_AGENT_REFERENCES, REQUIRED_SCAFFOLD_PATHS

    root_value = config.get("root", ".")
    if not isinstance(root_value, str):
        raise ValueError("root must be a string")
    ROOT = (resolved.parent / root_value).resolve()

    canonical = config.get("canonical_policy_file", CANONICAL_POLICY_FILE)
    active_agents = config.get("active_agent_directory", ACTIVE_AGENT_DIRECTORY)
    if not isinstance(canonical, str):
        raise ValueError("canonical_policy_file must be a string")
    if active_agents is not None and not isinstance(active_agents, str):
        raise ValueError("active_agent_directory must be a string or null")
    CANONICAL_POLICY_FILE = canonical
    ACTIVE_AGENT_DIRECTORY = active_agents
    SCHEMA_LOCATIONS = _string_list(config, "schema_locations", SCHEMA_LOCATIONS)
    REQUIRED_METADATA = _string_list(config, "required_metadata", REQUIRED_METADATA)
    TEMPLATE_GLOBS = _string_list(config, "template_globs", TEMPLATE_GLOBS)
    DOCUMENT_CONTROL_INCLUDE = _string_list(
        config, "document_control_include", DOCUMENT_CONTROL_INCLUDE
    )
    DOCUMENT_CONTROL_EXCLUDE = _string_list(
        config, "document_control_exclude", DOCUMENT_CONTROL_EXCLUDE
    )
    REQUIRED_SCAFFOLD_PATHS = _string_list(
        config, "required_scaffold_paths", REQUIRED_SCAFFOLD_PATHS
    )

    enforce_types = config.get("enforce_agent_template_types", False)
    if not isinstance(enforce_types, bool):
        raise ValueError("enforce_agent_template_types must be true or false")
    ENFORCE_AGENT_TEMPLATE_TYPES = enforce_types

    pattern_values = _string_list(config, "private_path_patterns", (r"\.agents/",))
    try:
        PRIVATE_PATH_PATTERNS = tuple(re.compile(pattern) for pattern in pattern_values)
    except re.error as exc:
        raise ValueError(f"invalid private_path_patterns regular expression: {exc}") from exc

    exception_values = config.get("approved_exceptions", {})
    if not isinstance(exception_values, dict):
        raise ValueError("approved_exceptions must be an object keyed by repository path")
    compiled_exceptions: dict[str, tuple[re.Pattern[str], ...]] = {}
    try:
        for path, patterns in exception_values.items():
            if not isinstance(path, str) or not isinstance(patterns, list) or not all(
                isinstance(pattern, str) for pattern in patterns
            ):
                raise ValueError(
                    "approved_exceptions values must be arrays of regular-expression strings"
                )
            compiled_exceptions[path] = tuple(re.compile(pattern) for pattern in patterns)
    except re.error as exc:
        raise ValueError(f"invalid approved_exceptions regular expression: {exc}") from exc
    APPROVED_HIDDEN_AGENT_REFERENCES = compiled_exceptions


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.relative_to(ROOT).parts
    )


def configured_files(patterns: tuple[str, ...]) -> list[Path]:
    files: set[Path] = set()
    for pattern in patterns:
        files.update(path for path in ROOT.glob(pattern) if path.is_file())
    return sorted(path for path in files if ".git" not in path.relative_to(ROOT).parts)


def template_files() -> list[Path]:
    return configured_files(TEMPLATE_GLOBS)


def document_control_files() -> list[Path]:
    included = set(configured_files(DOCUMENT_CONTROL_INCLUDE))
    excluded = set(configured_files(DOCUMENT_CONTROL_EXCLUDE))
    return sorted(included - excluded)


def rendered_lines(path: Path):
    """Yield non-code Markdown lines with one-based line numbers."""
    in_fence = False
    fence_token = ""

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence = FENCE.match(line)
        if fence:
            token = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            continue

        if in_fence or line.startswith("    ") or line.startswith("\t"):
            continue

        yield line_number, line


def extract_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def exact_relative_path(source: Path, target: str) -> tuple[bool, str]:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return True, "external target"
    if target.startswith("#"):
        return True, "anchor-only target"

    repository_absolute = target.startswith("/")
    decoded_path = unquote(
        parsed.path.lstrip("/") if repository_absolute else parsed.path
    )
    if not decoded_path:
        return True, "repository root" if repository_absolute else "anchor-only target"

    source_dir = Path() if repository_absolute else source.parent.relative_to(ROOT)
    normalized = Path(os.path.normpath(source_dir / decoded_path))
    if normalized.parts and normalized.parts[0] == "..":
        return False, f"target escapes repository: {target}"

    current = ROOT
    for part in normalized.parts:
        if not current.is_dir():
            return False, f"parent is not a directory: {current.relative_to(ROOT)}"

        names = {entry.name for entry in current.iterdir()}
        if part not in names:
            case_matches = sorted(name for name in names if name.casefold() == part.casefold())
            if case_matches:
                return False, f"case mismatch: {part} should be {case_matches[0]}"
            return False, f"missing target component: {part}"
        current /= part

    return True, "resolved"


def check_links(files: list[Path]) -> tuple[int, list[str]]:
    checked = 0
    failures: list[str] = []

    for path in files:
        relative_path = path.relative_to(ROOT)
        for line_number, line in rendered_lines(path):
            targets = [match.group(1) for match in MARKDOWN_LINK.finditer(line)]
            reference = REFERENCE_LINK.match(line)
            if reference:
                targets.append(reference.group(1))

            for raw_target in targets:
                target = extract_target(raw_target)
                ok, reason = exact_relative_path(path, target)
                if reason.startswith(("external", "anchor-only")):
                    continue
                checked += 1
                if not ok:
                    failures.append(f"{relative_path}:{line_number}: {target}: {reason}")

    return checked, failures


def check_agent_paths(files: list[Path]) -> tuple[int, int, list[str]]:
    candidates = 0
    approved = 0
    failures: list[str] = []

    if ACTIVE_AGENT_DIRECTORY and not (ROOT / ACTIVE_AGENT_DIRECTORY).is_dir():
        failures.append(f"{ACTIVE_AGENT_DIRECTORY}/: active agent directory is missing")
    if ACTIVE_AGENT_DIRECTORY == "agents/templates" and (ROOT / ".agents").exists():
        failures.append(".agents/: competing hidden template directory must not exist here")

    for path in files:
        relative_path = str(path.relative_to(ROOT))
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if DOUBLED_AGENT_SEPARATOR.search(line):
                failures.append(f"{relative_path}:{line_number}: doubled agent-folder separator")

            if not any(pattern.search(line) for pattern in PRIVATE_PATH_PATTERNS):
                continue

            candidates += 1
            patterns = APPROVED_HIDDEN_AGENT_REFERENCES.get(relative_path, ())
            if any(pattern.search(line) for pattern in patterns):
                approved += 1
            else:
                failures.append(
                    f"{relative_path}:{line_number}: unapproved private-path reference candidate"
                )

    return candidates, approved, failures


def check_required_scaffolds() -> tuple[int, list[str]]:
    failures: list[str] = []

    required_paths = tuple(dict.fromkeys((CANONICAL_POLICY_FILE, *REQUIRED_SCAFFOLD_PATHS)))
    for relative_path in required_paths:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path}: required scaffold file is missing")

    return len(required_paths), failures


def parse_document_control(path: Path) -> tuple[str, str, str | None]:
    text = path.read_text(encoding="utf-8")
    heading_offsets = [
        index
        for index, line in rendered_lines(path)
        if line.strip() == "## Document control"
    ]
    if not heading_offsets:
        return "", "", "missing Document control section"
    if len(heading_offsets) != 1:
        return "", "", "must contain exactly one Document control section"

    lines = text.splitlines()
    control_start = heading_offsets[0] - 1
    control = lines[control_start:]
    version = ""
    last_edited = ""

    for line in control:
        plain = line.strip().replace("**", "")
        if plain.startswith("Last edited:"):
            last_edited = plain.split(":", 1)[1].strip()
        elif plain.startswith("Current version:"):
            version = plain.split(":", 1)[1].strip()

    if not DOCUMENT_VERSION.fullmatch(version):
        return version, last_edited, "current document version must use MAJOR.MINOR"
    if not ISO_DATE.fullmatch(last_edited):
        return version, last_edited, "last-edited date must use YYYY-MM-DD"
    try:
        date.fromisoformat(last_edited)
    except ValueError:
        return version, last_edited, "last-edited date is not a real calendar date"

    matching_history_rows = 0
    history_versions: dict[str, str] = {}
    for line in control:
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if DOCUMENT_VERSION.fullmatch(cells[0]):
            if cells[0] in history_versions:
                return version, last_edited, f"history reuses document version {cells[0]}"
            if not ISO_DATE.fullmatch(cells[1]):
                return version, last_edited, f"history date for {cells[0]} must use YYYY-MM-DD"
            try:
                date.fromisoformat(cells[1])
            except ValueError:
                return version, last_edited, f"history date for {cells[0]} is not real"
            if not cells[2]:
                return version, last_edited, f"history summary for {cells[0]} is empty"
            history_versions[cells[0]] = cells[1]
        if cells[0] == version and cells[1] == last_edited and cells[2]:
            matching_history_rows += 1

    if matching_history_rows != 1:
        return (
            version,
            last_edited,
            "current version/date must have exactly one matching non-empty history row",
        )

    current_parts = tuple(int(part) for part in version.split("."))
    newest_parts = max(
        tuple(int(part) for part in historical_version.split("."))
        for historical_version in history_versions
    )
    if current_parts != newest_parts:
        return version, last_edited, "current document version is not the highest history version"

    return version, last_edited, None


def check_document_controls(files: list[Path]) -> tuple[int, list[str]]:
    failures: list[str] = []

    for path in files:
        _, _, error = parse_document_control(path)
        if error:
            failures.append(f"{path.relative_to(ROOT)}: {error}")

    return len(files), failures


def parse_metadata_scalar(value: str) -> tuple[object, str | None]:
    """Parse the simple YAML scalar subset allowed in template metadata."""
    if not value:
        return "", None

    if value.startswith('"'):
        if not value.endswith('"'):
            return "", "unterminated double-quoted string"
        try:
            parsed = json_loads(value)
        except JSONDecodeError as exc:
            return "", f"invalid double-quoted string: {exc.msg}"
        if not isinstance(parsed, str):
            return "", "double-quoted metadata values must be strings"
        return parsed, None

    if value.startswith("'"):
        if not value.endswith("'"):
            return "", "unterminated single-quoted string"
        return value[1:-1].replace("''", "'"), None

    if value.endswith(('"', "'")):
        return "", "unmatched quote in metadata value"

    lowered = value.casefold()
    if lowered in {"true", "false"}:
        return lowered == "true", None
    if lowered in {"null", "~"}:
        return None, None
    if PLAIN_INTEGER.fullmatch(value):
        return int(value), None
    if PLAIN_FLOAT.fullmatch(value):
        return float(value), None
    if ISO_DATE.fullmatch(value):
        try:
            return date.fromisoformat(value), None
        except ValueError:
            return value, None

    return value, None


def parse_template_metadata(path: Path) -> tuple[dict[str, object], str | None]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end == -1:
            return {}, "missing closing YAML frontmatter delimiter"
        block = text[4:end]
    elif text.startswith("<!--\n"):
        end = text.find("\n-->\n", 5)
        if end == -1:
            return {}, "missing closing metadata-comment delimiter"
        block = text[5:end]
    else:
        return {}, "missing leading schema metadata"

    metadata: dict[str, object] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"unsupported metadata line: {line}"
        key, value = line.split(":", 1)
        key = key.strip()
        raw_value = value.strip()
        if not key or key in metadata:
            return {}, f"invalid or duplicate metadata key: {key or '<blank>'}"
        parsed_value, value_error = parse_metadata_scalar(raw_value)
        if value_error:
            return {}, f"{key}: {value_error}"
        metadata[key] = parsed_value

    return metadata, None


def discover_schema_versions() -> tuple[set[int], list[str]]:
    versions: set[int] = set()
    failures: list[str] = []
    for location in SCHEMA_LOCATIONS:
        schemas_root = ROOT / location
        if not schemas_root.is_dir():
            failures.append(f"{location}/: schema directory is missing")
            continue

        for path in sorted(schemas_root.iterdir()):
            match = SCHEMA_DIRECTORY.fullmatch(path.name)
            if not path.is_dir() or not match:
                continue
            version = int(match.group(1))
            versions.add(version)
            required_files = ("README.md", "INTRODUCED.md", "schema-contract.template.md")
            for required_name in required_files:
                if not (path / required_name).is_file():
                    failures.append(
                        f"{location}/{path.name}/{required_name}: required version scaffold is missing"
                    )

    if not versions:
        failures.append("configured schema locations: no supported vN directories found")
        return versions, failures

    expected_versions = set(range(1, max(versions) + 1))
    for missing_version in sorted(expected_versions - versions):
        failures.append(f"configured schemas/v{missing_version}/: schema version sequence has a gap")

    return versions, failures


def check_template_versions() -> tuple[int, int, list[str]]:
    files = template_files()
    supported_versions, failures = discover_schema_versions()
    latest_version = max(supported_versions) if supported_versions else 0

    for path in files:
        relative_path = str(path.relative_to(ROOT))
        metadata, error = parse_template_metadata(path)
        if error:
            failures.append(f"{relative_path}: {error}")
            continue

        for key in REQUIRED_METADATA:
            if key not in metadata:
                failures.append(f"{relative_path}: required metadata key {key} is missing")

        schema_version = metadata.get("schema_version")
        if "schema_version" in metadata and type(schema_version) is not int:
            failures.append(
                f"{relative_path}: schema_version must be an unquoted integer"
            )
        elif "schema_version" in metadata and schema_version not in supported_versions:
            failures.append(
                f"{relative_path}: unsupported schema_version {schema_version}; "
                f"available versions are {sorted(supported_versions)}"
            )

        relative = path.relative_to(ROOT)
        schema_location = str(relative.parent.parent) if len(relative.parts) >= 3 else ""
        versioned_schema = (
            relative.name == "schema-contract.template.md"
            and schema_location in SCHEMA_LOCATIONS
            and SCHEMA_DIRECTORY.fullmatch(relative.parent.name)
        )
        if versioned_schema and type(schema_version) is int:
            directory_version = int(relative.parent.name[1:])
            if schema_version != directory_version:
                failures.append(
                    f"{relative_path}: schema_version must match its v{directory_version} directory"
                )

        template_type = metadata.get("type")
        if "type" in metadata and not isinstance(template_type, str):
            failures.append(f"{relative_path}: type must be a string")
        elif (
            "type" in metadata
            and ENFORCE_AGENT_TEMPLATE_TYPES
            and template_type not in ALLOWED_TEMPLATE_TYPES
        ):
            failures.append(f"{relative_path}: unsupported or missing template type")

        expected_type = EXPECTED_TEMPLATE_TYPES.get(relative_path) if ENFORCE_AGENT_TEMPLATE_TYPES else None
        if (
            ENFORCE_AGENT_TEMPLATE_TYPES
            and ACTIVE_AGENT_DIRECTORY
            and relative_path.startswith(f"{ACTIVE_AGENT_DIRECTORY}/")
        ):
            expected_type = "agent_role"
        elif ENFORCE_AGENT_TEMPLATE_TYPES and versioned_schema:
            expected_type = "schema_contract"
        if expected_type and template_type != expected_type:
            failures.append(
                f"{relative_path}: type must be {expected_type} (received {template_type or '<missing>'})"
            )

        template_id = metadata.get("template_id")
        if "template_id" in metadata and not isinstance(template_id, str):
            failures.append(f"{relative_path}: template_id must be a string")
        elif isinstance(template_id, str) and not TEMPLATE_ID.fullmatch(template_id):
            failures.append(f"{relative_path}: template_id must be a stable lower-case slug")

        document_version = metadata.get("document_version")
        if "document_version" in metadata and not isinstance(document_version, str):
            failures.append(
                f"{relative_path}: document_version must be a quoted string"
            )
        elif isinstance(document_version, str) and not DOCUMENT_VERSION.fullmatch(document_version):
            failures.append(f"{relative_path}: document_version must use MAJOR.MINOR")

        last_edited = metadata.get("last_edited")
        if "last_edited" in metadata and not isinstance(last_edited, str):
            failures.append(f"{relative_path}: last_edited must be a quoted date string")
        elif isinstance(last_edited, str) and not ISO_DATE.fullmatch(last_edited):
            failures.append(f"{relative_path}: last_edited must use YYYY-MM-DD")
        elif isinstance(last_edited, str):
            try:
                date.fromisoformat(last_edited)
            except ValueError:
                failures.append(f"{relative_path}: last_edited is not a real date")

        controlled_version, controlled_date, control_error = parse_document_control(path)
        if control_error is None:
            if "document_version" in metadata and document_version != controlled_version:
                failures.append(
                    f"{relative_path}: metadata and control-block document versions differ"
                )
            if "last_edited" in metadata and last_edited != controlled_date:
                failures.append(
                    f"{relative_path}: metadata and control-block last-edited dates differ"
                )

        if template_type == "agent_role":
            role = metadata.get("role")
            if not isinstance(role, str):
                failures.append(f"{relative_path}: agent_role role must be a string")
            elif not TEMPLATE_ID.fullmatch(role):
                failures.append(f"{relative_path}: agent_role requires a lower-case role slug")

    return len(files), latest_version, failures


def main() -> int:
    try:
        apply_configuration(parse_arguments().config)
    except ValueError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    files = markdown_files()
    link_count, link_failures = check_links(files)
    path_candidates, approved_candidates, path_failures = check_agent_paths(files)
    scaffold_count, scaffold_failures = check_required_scaffolds()
    controlled_files = document_control_files()
    document_count, document_failures = check_document_controls(controlled_files)
    template_count, latest_schema_version, template_failures = check_template_versions()
    failures = (
        link_failures
        + path_failures
        + scaffold_failures
        + document_failures
        + template_failures
    )

    print(f"Markdown files scanned: {len(files)}")
    print(f"Relative Markdown links resolved: {link_count}")
    print(
        "Private-path candidates: "
        f"{path_candidates} ({approved_candidates} approved exceptions)"
    )
    present_count = scaffold_count - len(scaffold_failures)
    print(f"Required scaffold files present: {present_count}/{scaffold_count}")
    print(f"Document controls checked: {document_count}")
    print(f"Versioned reusable templates checked: {template_count}")
    print(f"Latest supported schema version: {latest_schema_version or 'none'}")

    if failures:
        print("\nDocumentation validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
