# Agent Template

A reusable, tool-neutral operating-contract template for future projects.

## Use

1. Copy AGENTS.template.md into a new repository as AGENTS.md.
2. Replace every [CUSTOMIZE] field.
3. Remove optional sections that do not apply.
4. Copy VERSIONING.template.md to VERSIONING.md when the project has schemas,
   releases, migrations, or versioned deliverables; customize its version
   surfaces and owners.
5. Keep the versioned [schemas/v1/](schemas/v1/) baseline. Copy
   [schema-contract.template.md](schemas/v1/schema-contract.template.md) for each
   shared data or interface contract and register it in the version index.
6. Apply the [document-control contract](schemas/v1/document-control.md) to every
   durable human-authored file. Give each one a distinct content version,
   last-edited date, and append-only change history.
7. Keep AGENTS.md canonical. Make CLAUDE.md and other runtime entry files thin
   pointers rather than divergent copies.
8. Commit the customized contract on a feature branch and review it like code.

The included [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
keeps schema, version, validation, Git, and human approval evidence visible at
the review boundary.

Example:

    cp AGENTS.template.md /path/to/project/AGENTS.md
    cp VERSIONING.template.md /path/to/project/VERSIONING.md
    mkdir -p /path/to/project/schemas/v1
    cp schemas/v1/schema-contract.template.md /path/to/project/schemas/v1/example.md

## Improve an existing repository

Use [ADOPTION.md](ADOPTION.md) when a future agent should compare an existing
repository with the current `Agent-Template/main` guidance.

The workflow is audit-first and practice-based. It records the exact template
and local commits, writes an incremental adoption matrix, preserves stricter or
project-specific rules, and proposes exact changes before editing local
`AGENTS.md` or `CLAUDE.md`. Authorized changes are made minimally on a feature
branch, with `AGENTS.md` updated before its tool-specific adapters.

## Included sub-agent templates

Reusable role guides live under [agents/templates/](agents/templates/). Start
with the smallest team that has distinct owned outputs.

Every role template carries v1 YAML metadata. Preserve `schema_version`, `type`,
`template_id`, and `role` when copying it. Start the copied document's own
`document_version`, `last_edited` value, and history under the downstream
project's policy. Replace the role identity only when customizing the role
skeleton; create a new schema version rather than silently changing what an
existing metadata field means.

| Role | Best used for |
| --- | --- |
| [Role skeleton](agents/templates/role-skeleton.template.md) | A project-specific specialist that does not fit a starter role |
| [Orchestrator](agents/templates/orchestrator.template.md) | Routing, prerequisite gates, user questions, cross-file validation, and commits |
| [Schema / Version Steward](agents/templates/schema-version-steward.template.md) | Shared contracts, compatibility, migrations, and version-bump proposals |
| [Researcher](agents/templates/researcher.template.md) | Bounded, source-backed research written one completed question at a time |
| [Writer / Implementer](agents/templates/writer-implementer.template.md) | Producing one approved prose artifact, document, code surface, or directly owned test |
| [Reviewer / Critic](agents/templates/reviewer-critic.template.md) | Independent, anchored findings without modifying the artifact |
| [Validator / Auditor](agents/templates/validator-auditor.template.md) | Reproducible PASS, FAIL, NOT ASSESSABLE, or NOT REQUIRED gate results |
| [Privacy / Risk Gate](agents/templates/privacy-risk-gate.template.md) | Pre-plan and final-diff veto for sensitive or high-risk work |

The [agents selection guide](agents/README.md) explains when each role earns
its place, common team shapes, handoff formats, sequencing, runtime adapters, and
degraded-mode behavior.

Example:

    mkdir -p /path/to/project/agents
    cp agents/templates/orchestrator.template.md /path/to/project/agents/orchestrator.md
    cp agents/templates/researcher.template.md /path/to/project/agents/researcher.md

## What the template carries forward

- Git-first work on feature branches, logical commits, pull requests, CI
  follow-through, and no agent-initiated merge.
- Distinct schema, release, deliverable, migration, and Git version surfaces
  with explicit owners, compatibility rules, and traceability.
- Integer-versioned `schemas/vN/` contracts; every reusable template declares
  its `schema_version`, stable `type`, and identity.
- Per-file document control for durable human-authored artifacts: two-part
  content version, last-edited date, and append-only change history kept
  distinct from schema, release, migration, and Git revisions.
- Canonical schema contracts with producer/consumer inventories, explicit
  unknown/legacy behavior, synthetic fixtures, migration gates, and
  generated-drift checks.
- A pull-request checklist that makes version decisions, checks, release state,
  and human-only merge authority reviewable.
- Durable checkpoints after each natural unit and interruption-safe resume.
- Clear folder boundaries for framework, private input, work state, generated
  output, templates, examples, research, tests, and archives.
- Evidence-first research with sources, check dates, confidence, and unknowns
  written as the research proceeds.
- Minimal diffs, explicit ownership, structured handoffs, prerequisite gates,
  proportional re-review, and binary readiness criteria.
- Strong privacy boundaries and pre-draft/final-diff gates for work derived from
  sensitive sources.
- Read-only audit, reviewable manifests, approval binding, collision refusal,
  and independent validation for high-risk filesystem changes.
- Versioned deliverables that preserve superseded files rather than overwriting
  history.

## Validate the template

Run the same documentation check used by CI:

    python3 scripts/check_template_docs.py

The check resolves relative Markdown links with exact case, confirms the active
visible `agents/` template tree, rejects doubled separators and unapproved hidden
agent-folder references, and adjudicates intentional `.agents/` discussion
through explicit approved exceptions rather than treating every scanner match
as a failure. It also requires the schema, versioning, and schema-steward
scaffold files, checks document-control blocks on every Markdown file, and
verifies the schema and document metadata on every reusable template.

## Review basis

This template synthesizes repeated practices observed across multiple projects.
The source corpus and repository identities are intentionally not published.
Only portable, project-neutral working agreements belong in this public
scaffold; project-specific facts, paths, and operating details stay in their
source repositories.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Added public schema, role, adoption, and per-file document-version scaffolding. |
