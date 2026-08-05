#!/usr/bin/env python3
"""Validate Markdown links, agent paths, schemas, and document controls."""

from __future__ import annotations

import os
import re
import sys
from datetime import date
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

TEMPLATE_SCHEMA_VERSION = "1"
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
    "schemas/v1/schema-contract.template.md": "schema_contract",
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
    if parsed.scheme or parsed.netloc or target.startswith(("#", "/")):
        return True, "external, anchor, or repository-absolute target"

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return True, "anchor-only target"

    source_dir = source.parent.relative_to(ROOT)
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

    lines = text.splitlines()
    control_start = heading_offsets[-1] - 1
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


def parse_template_metadata(path: Path) -> tuple[dict[str, str], str | None]:
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

    metadata: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"unsupported metadata line: {line}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or key in metadata:
            return {}, f"invalid or duplicate metadata key: {key or '<blank>'}"
        metadata[key] = value

    return metadata, None


def check_template_versions() -> tuple[int, list[str]]:
    files = template_files()
    failures: list[str] = []

    for path in files:
        relative_path = str(path.relative_to(ROOT))
        metadata, error = parse_template_metadata(path)
        if error:
            failures.append(f"{relative_path}: {error}")
            continue

        schema_version = metadata.get("schema_version")
        if schema_version != TEMPLATE_SCHEMA_VERSION:
            failures.append(
                f"{relative_path}: schema_version must be {TEMPLATE_SCHEMA_VERSION}"
            )

        template_type = metadata.get("type", "")
        if template_type not in ALLOWED_TEMPLATE_TYPES:
            failures.append(f"{relative_path}: unsupported or missing template type")

        expected_type = EXPECTED_TEMPLATE_TYPES.get(relative_path)
        if relative_path.startswith("agents/templates/"):
            expected_type = "agent_role"
        if expected_type and template_type != expected_type:
            failures.append(
                f"{relative_path}: type must be {expected_type} (received {template_type or '<missing>'})"
            )

        template_id = metadata.get("template_id", "")
        if not TEMPLATE_ID.fullmatch(template_id):
            failures.append(f"{relative_path}: template_id must be a stable lower-case slug")

        document_version = metadata.get("document_version", "")
        if not DOCUMENT_VERSION.fullmatch(document_version):
            failures.append(f"{relative_path}: document_version must use MAJOR.MINOR")

        last_edited = metadata.get("last_edited", "")
        if not ISO_DATE.fullmatch(last_edited):
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
            role = metadata.get("role", "")
            if not TEMPLATE_ID.fullmatch(role):
                failures.append(f"{relative_path}: agent_role requires a lower-case role slug")

    return len(files), failures


def main() -> int:
    files = markdown_files()
    link_count, link_failures = check_links(files)
    path_candidates, approved_candidates, path_failures = check_agent_paths(files)
    scaffold_count, scaffold_failures = check_required_scaffolds()
    document_count, document_failures = check_document_controls(files)
    template_count, template_failures = check_template_versions()
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

    if failures:
        print("\nDocumentation validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
