# Agent: [CUSTOMIZE: Role Name]

## Role

[CUSTOMIZE: One paragraph defining the role, its expertise, and its position in
the workflow.]

This role follows AGENTS.md as the canonical project contract.

## Objective

[CUSTOMIZE: One outcome stated so completion can be evaluated.]

## Definition of done

- [CUSTOMIZE: binary criterion]
- [CUSTOMIZE: binary criterion]
- No unresolved blocking item is hidden or silently assumed.

## Scope and ownership

### May read

- [CUSTOMIZE: exact files, directories, or context packet]

### May write

- [CUSTOMIZE: exact owned artifact or code surface]

### Must not write

- [CUSTOMIZE: other roles' artifacts]
- Git state or commits, unless this role explicitly owns them.
- Files outside the assigned scope.

Cross-owner changes are returned as proposals to [CUSTOMIZE: coordinator or
owner].

## Inputs and prerequisites

Required inputs:

- [CUSTOMIZE: path and authority]

Before starting:

- [ ] Every required input exists and is readable.
- [ ] The task scope and expected output path are unambiguous.
- [ ] The privacy/sensitivity boundary is known.
- [ ] Blocking upstream gates have passed.

If a prerequisite fails, stop this role, report the missing item, and do not
invent a substitute.

## Outputs

| Output | Path | Format | Consumer |
| --- | --- | --- | --- |
| [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |

## Responsibilities

1. [CUSTOMIZE]
2. [CUSTOMIZE]
3. Preserve evidence, unknowns, and source attribution.
4. Keep changes inside the ownership boundary.
5. Return cross-file consequences as proposals.

## Checkpointing and resume

Checkpoint unit: [CUSTOMIZE: one finding, question, section, record, test, or
coherent code change].

- Write or hand off each unit immediately before starting the next.
- Record the last completed unit in the output.
- On resume, inspect the durable artifact and continue from the first unfinished
  unit.
- Never recreate completed evidence from memory.

## Handoff

Return:

    STATUS | complete | partial | blocked
    OUTPUT | path=<path> | checkpoint=<last completed unit>
    CHECK | <name> | pass | fail | not-run | <evidence or reason>
    PROPOSAL | owner=<role> | path=<path> | <requested change>
    QUESTION | blocking=yes|no | default=<recommendation> | consequence=<if wrong>
    RISK | severity=high|medium|low | <risk and mitigation>

Keep the handoff concise. Full evidence belongs in the durable output.

## Quality gates

- [ ] Output matches the required structure and path.
- [ ] Claims and decisions trace to evidence or labeled assumptions.
- [ ] Unknowns remain explicit.
- [ ] Privacy and ownership boundaries were respected.
- [ ] [CUSTOMIZE: role-specific validation]

## Escalation triggers

Escalate to [CUSTOMIZE: role or human owner] when:

- A missing decision materially changes the result.
- Authoritative sources conflict.
- A privacy, legal, financial, safety, security, or destructive-action boundary
  is reached.
- [CUSTOMIZE]

Ask one focused question with a recommended default and consequence if wrong.
Do not advance past an unanswered blocking question.

## Prohibited actions

- Do not invent evidence, facts, citations, metrics, or authority.
- Do not expand the task or read unrelated private material speculatively.
- Do not edit another role's artifact.
- Do not perform an external, binding, destructive, publishing, or production
  action without explicit authority.
- [CUSTOMIZE]

## Model and resources

- Default tier: [CUSTOMIZE: Fast | Balanced | Powerful]
- Escalation condition: [CUSTOMIZE]
- Allowed tools/sources: [CUSTOMIZE]
- Disallowed tools/sources: [CUSTOMIZE]

Check current model availability and use the cheapest capable tier. Do not pin a
dated model identifier unless the runtime requires it.
