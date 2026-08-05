# Agent Template Maintenance Contract

This file governs work on the Agent-Template repository itself. The reusable
downstream contract remains `AGENTS.template.md`.

## Scope and authority

- Keep this repository public, project-neutral, and free of private repository
  names, private facts, credentials, and local absolute user paths.
- Treat `AGENTS.template.md`, `VERSIONING.template.md`, `agents/templates/`, and
  `schemas/vN/` as reusable public interfaces.
- Do not merge pull requests. A human owns merge, release, repository visibility,
  and other administrative decisions unless the user explicitly authorizes a
  narrower action.
- Preserve unrelated work, local stashes, and user-owned branches.

## Git workflow

1. Start from an updated `main` and inspect branch, worktree, upstream, and
   remotes before editing.
2. Work on a feature branch using the repository's documented prefix convention.
3. Write and validate one coherent unit at a time.
4. Stage only reviewed files, use logical commits, push the feature branch, and
   open a pull request against `main`.
5. Report the actual branch, commit, PR, CI state, and remaining unknowns.

## Schema and document control

- Every reusable template declares typed metadata governed by a supported
  `schemas/vN/` contract.
- A schema version is an unquoted positive integer. String-valued versions and
  dates that resemble YAML numbers or dates remain quoted strings.
- Breaking contract changes create the next integer `schemas/vN/` directory;
  do not rewrite a released major version into a different shape.
- Every durable human-authored Markdown file has exactly one `## Document
  control` section with a current version, matching last-edited date, and one
  matching history row.
- Ordinary content changes advance the document version without changing the
  schema version. Keep schema, document, release, migration, and Git revisions
  distinct.

## Validation

Run before handoff:

    python3 scripts/check_template_docs.py
    python3 -m unittest discover -s tests -v
    git diff --check

When changing the validator, add or update a positive or negative fixture that
proves the intended behavior. Treat scanner matches as candidates, then check
them against authoritative files and approved exceptions.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established maintenance rules for the public template repository. |
