#!/usr/bin/env python3
"""Validate Markdown links, agent paths, schemas, and document controls."""

from __future__ import annotations

import os
import re
import sys
from datetime import date
from json import JSONDecodeError, loads as json_loads
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
FENCE = re.compile(r"^\s*(```|~~~)")
HIDDEN_AGENT_REFERENCE = re.compile(r"\.agents/")
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


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.relative_to(ROOT).parts
    )


def template_files() -> list[Path]:
    files = {
        path
        for path in ROOT.rglob("*.template.md")
        if ".git" not in path.relative_to(ROOT).parts
    }
    pull_request_template = ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
    if pull_request_template.is_file():
        files.add(pull_request_template)
    return sorted(files)


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

    if not (ROOT / "agents" / "templates").is_dir():
        failures.append("agents/templates/: required visible template directory is missing")
    if (ROOT / ".agents").exists():
        failures.append(".agents/: competing hidden template directory must not exist here")

    for path in files:
        relative_path = str(path.relative_to(ROOT))
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if DOUBLED_AGENT_SEPARATOR.search(line):
                failures.append(f"{relative_path}:{line_number}: doubled agent-folder separator")

            if not HIDDEN_AGENT_REFERENCE.search(line):
                continue

            candidates += 1
            patterns = APPROVED_HIDDEN_AGENT_REFERENCES.get(relative_path, ())
            if any(pattern.search(line) for pattern in patterns):
                approved += 1
            else:
                failures.append(
                    f"{relative_path}:{line_number}: unapproved .agents/ reference candidate"
                )

    return candidates, approved, failures


def check_required_scaffolds() -> tuple[int, list[str]]:
    failures: list[str] = []

    for relative_path in REQUIRED_SCAFFOLD_PATHS:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path}: required scaffold file is missing")

    return len(REQUIRED_SCAFFOLD_PATHS), failures


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
    schemas_root = ROOT / "schemas"

    if not schemas_root.is_dir():
        return versions, ["schemas/: schema directory is missing"]

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
                    f"schemas/{path.name}/{required_name}: required version scaffold is missing"
                )

    if not versions:
        failures.append("schemas/: no supported vN schema directories found")
        return versions, failures

    expected_versions = set(range(1, max(versions) + 1))
    for missing_version in sorted(expected_versions - versions):
        failures.append(f"schemas/v{missing_version}/: schema version sequence has a gap")

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

        schema_version = metadata.get("schema_version")
        if type(schema_version) is not int:
            failures.append(
                f"{relative_path}: schema_version must be an unquoted integer"
            )
        elif schema_version not in supported_versions:
            failures.append(
                f"{relative_path}: unsupported schema_version {schema_version}; "
                f"available versions are {sorted(supported_versions)}"
            )

        versioned_schema_path = re.fullmatch(
            r"schemas/v([1-9][0-9]*)/schema-contract\.template\.md", relative_path
        )
        if versioned_schema_path and type(schema_version) is int:
            directory_version = int(versioned_schema_path.group(1))
            if schema_version != directory_version:
                failures.append(
                    f"{relative_path}: schema_version must match its v{directory_version} directory"
                )

        template_type = metadata.get("type")
        if not isinstance(template_type, str):
            failures.append(f"{relative_path}: type must be a string")
        elif template_type not in ALLOWED_TEMPLATE_TYPES:
            failures.append(f"{relative_path}: unsupported or missing template type")

        expected_type = EXPECTED_TEMPLATE_TYPES.get(relative_path)
        if relative_path.startswith("agents/templates/"):
            expected_type = "agent_role"
        elif versioned_schema_path:
            expected_type = "schema_contract"
        if expected_type and template_type != expected_type:
            failures.append(
                f"{relative_path}: type must be {expected_type} (received {template_type or '<missing>'})"
            )

        template_id = metadata.get("template_id")
        if not isinstance(template_id, str):
            failures.append(f"{relative_path}: template_id must be a string")
        elif not TEMPLATE_ID.fullmatch(template_id):
            failures.append(f"{relative_path}: template_id must be a stable lower-case slug")

        document_version = metadata.get("document_version")
        if not isinstance(document_version, str):
            failures.append(
                f"{relative_path}: document_version must be a quoted string"
            )
        elif not DOCUMENT_VERSION.fullmatch(document_version):
            failures.append(f"{relative_path}: document_version must use MAJOR.MINOR")

        last_edited = metadata.get("last_edited")
        if not isinstance(last_edited, str):
            failures.append(f"{relative_path}: last_edited must be a quoted date string")
        elif not ISO_DATE.fullmatch(last_edited):
            failures.append(f"{relative_path}: last_edited must use YYYY-MM-DD")
        else:
            try:
                date.fromisoformat(last_edited)
            except ValueError:
                failures.append(f"{relative_path}: last_edited is not a real date")

        controlled_version, controlled_date, control_error = parse_document_control(path)
        if control_error is None:
            if document_version != controlled_version:
                failures.append(
                    f"{relative_path}: metadata and control-block document versions differ"
                )
            if last_edited != controlled_date:
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
    files = markdown_files()
    link_count, link_failures = check_links(files)
    path_candidates, approved_candidates, path_failures = check_agent_paths(files)
    scaffold_count, scaffold_failures = check_required_scaffolds()
    document_count, document_failures = check_document_controls(files)
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
        "Hidden agent-path candidates: "
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
