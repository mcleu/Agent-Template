# Agent Template

A reusable, tool-neutral operating-contract template for future projects.

## Use

1. Copy AGENTS.template.md into a new repository as AGENTS.md.
2. Replace every [CUSTOMIZE] field.
3. Remove optional sections that do not apply.
4. Keep AGENTS.md canonical. Make CLAUDE.md and other runtime entry files thin
   pointers rather than divergent copies.
5. Commit the customized contract on a feature branch and review it like code.

Example:

    cp AGENTS.template.md /path/to/project/AGENTS.md

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

| Role | Best used for |
| --- | --- |
| [Role skeleton](agents/templates/role-skeleton.template.md) | A project-specific specialist that does not fit a starter role |
| [Orchestrator](agents/templates/orchestrator.template.md) | Routing, prerequisite gates, user questions, cross-file validation, and commits |
| [Researcher](agents/templates/researcher.template.md) | Bounded, source-backed research written one completed question at a time |
| [Writer / Implementer](agents/templates/writer-implementer.template.md) | Producing one approved prose artifact, document, code surface, or directly owned test |
| [Reviewer / Critic](agents/templates/reviewer-critic.template.md) | Independent, anchored findings without modifying the artifact |
| [Validator / Auditor](agents/templates/validator-auditor.template.md) | Reproducible PASS, FAIL, or NOT ASSESSABLE exit gates |
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

## Review basis

The synthesis reviewed root contracts and the agent, workflow, command, skill,
schema, and collaboration guides one to two relevant guide layers deep in:

- HSA-Tracking
- mcleu.github.io
- ProductAgent
- PropertyAgent
- TripAgent
- PatentAgent
- mVault

The requested roots contained no authored ROBOTS.md operating guide. The only
robots.md found was framework documentation inside a Next.js dependency under
node_modules; it was inspected and excluded from the synthesis because it
describes search-engine metadata rather than project-working preferences.

Domain-specific details were not copied into the general contract. Patent,
travel, property, portfolio, medical-device, and vault rules appear only as
portable practices or optional modules.
