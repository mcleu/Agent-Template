#!/usr/bin/env python3
"""Validate repository Markdown links and active agent-folder references."""

from __future__ import annotations

import os
import re
import sys
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
    "schemas/v1/template-metadata.md",
    "schemas/v1/schema-contract.template.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "agents/README.md",
    "agents/templates/schema-version-steward.template.md",
)

TEMPLATE_SCHEMA_VERSION = "1"
TEMPLATE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
    template_count, template_failures = check_template_versions()
    failures = link_failures + path_failures + scaffold_failures + template_failures

    print(f"Markdown files scanned: {len(files)}")
    print(f"Relative Markdown links resolved: {link_count}")
    print(
        "Hidden agent-path candidates: "
        f"{path_candidates} ({approved_candidates} approved exceptions)"
    )
    present_count = scaffold_count - len(scaffold_failures)
    print(f"Required scaffold files present: {present_count}/{scaffold_count}")
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
