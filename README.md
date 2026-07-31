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
