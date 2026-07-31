# Reusable Sub-Agent Templates

These are tool-neutral role templates for projects that benefit from bounded,
specialized agents. Copy only the roles the project needs, customize every
placeholder, and keep the project's root AGENTS.md authoritative.

## Start small

Do not create a team merely because roles can be named. A separate agent earns
its place only when it has:

- A distinct objective and expertise.
- A bounded input packet.
- One clearly owned output or a read-only verdict.
- Work that can proceed independently or behind an explicit prerequisite gate.
- A checkpoint unit that can be written or handed off before interruption.
- A clear reason the main agent should not perform the work inline.

For a small task, use one agent and the root contract. For a multi-file,
high-risk, or interruption-prone workflow, begin with an Orchestrator plus the
smallest useful specialist set.

## Starter roles

| Template | Use when | Default mutation boundary |
| --- | --- | --- |
| [role-skeleton.template.md](templates/role-skeleton.template.md) | Creating a project-specific role not covered below | Must be customized |
| [orchestrator.template.md](templates/orchestrator.template.md) | Work has prerequisites, multiple owners, cross-file effects, or user decision gates | Coordinator-owned files and commits only |
| [researcher.template.md](templates/researcher.template.md) | A bounded question needs source-backed investigation | One assigned research file |
| [writer-implementer.template.md](templates/writer-implementer.template.md) | An approved plan or evidence set must become prose, code, or another artifact | One assigned artifact or code surface |
| [reviewer-critic.template.md](templates/reviewer-critic.template.md) | Independent critique is needed before acceptance | Findings only; read-only by default |
| [validator-auditor.template.md](templates/validator-auditor.template.md) | Completion claims must be independently tested against binary gates | Verdict/report only; read-only |
| [privacy-risk-gate.template.md](templates/privacy-risk-gate.template.md) | Sensitive sources, external publication, regulated work, or irreversible decisions require veto authority | Approval list and gate verdict only |

Common team shapes:

- Research task: Orchestrator → Researcher → Validator.
- Writing task: Orchestrator → Researcher, when needed → Writer → Reviewer.
- Coding task: Orchestrator → Writer/Implementer → Reviewer → Validator.
- Sensitive publication: Orchestrator → Researcher/Writer → Privacy Gate →
  Reviewer/Validator.
- High-risk migration: Orchestrator → independent inventory/classification →
  Privacy/Risk Gate → designated writer/runner → Validator.

## Shared contract for every role

Every project role must:

1. Read the root AGENTS.md and more-specific path contracts first.
2. Receive only the task-scoped context needed for its output.
3. Verify prerequisite files exist rather than trusting a completion message.
4. Own exactly the files named in its role guide.
5. Return cross-owner changes as proposals instead of editing another role's
   artifact.
6. Write each completed natural unit to disk, or hand it immediately to the
   Orchestrator when read-only.
7. Resume from the first unfinished unit by inspecting durable artifacts.
8. Preserve unknowns and distinguish evidence, inference, assumption, and
   recommendation.
9. Avoid external or binding actions unless the role and user authorization
   explicitly permit them.
10. Report blockers, degraded execution, and unverified checks plainly.

## Standard execution sequence

1. Frame the requested outcome, scope, source of truth, privacy boundary, and
   definition of done.
2. Assign every target artifact to one owner.
3. Create or identify the durable output before long research or writing.
4. Verify each role's input gate before dispatch.
5. Run independent read-only work in parallel when it will not create anchoring.
6. Serialize overlapping writes through the Orchestrator.
7. Validate each worker result before allowing its cross-file consequences.
8. Run changed artifacts through full review; scan unchanged artifacts only for
   stale cross-references.
9. Apply privacy/risk and independent validation gates where required.
10. Commit only validated files and report the actual branch, checks, and
    remaining unknowns.

## Handoff formats

Keep full evidence in each role's durable output. Give the Orchestrator a concise,
structured summary that can be merged without interpreting free-form prose.

Suggested worker handoff:

    STATUS | complete | partial | blocked
    OUTPUT | path=<path> | checkpoint=<last completed unit>
    CHECK | <check name> | pass | fail | not-run | <evidence or reason>
    PROPOSAL | owner=<role> | path=<path> | <requested cross-file change>
    QUESTION | blocking=yes|no | default=<recommendation> | consequence=<if wrong>
    RISK | severity=high|medium|low | <risk and mitigation>

Suggested review finding:

    FINDING | anchor=<path:line or stable ID> | severity=<high|medium|low>
    defect=<specific problem> | evidence=<why it is real>
    impact=<what fails> | proposal=<specific resolution>

Suggested validator verdict:

    VERDICT | PASS | FAIL | NOT ASSESSABLE
    GATE | <criterion> | pass|fail|not-assessable | evidence=<path, command, result>

Machine-consumable summaries should be capped to the most material findings.
The durable file may contain the complete analysis.

## Independence and sequencing

- An Orchestrator coordinates; it does not quietly become every specialist.
- Parallel reviewers should be blind to one another when shared context would
  create groupthink. The Orchestrator deduplicates after their reports exist.
- A Writer does not approve its own output.
- A Privacy/Risk Gate may block but does not rewrite the Writer's artifact.
- A Validator tests the actual final artifact and must not rely solely on the
  producer's reported checks.
- Specialists do not stage or commit unless they own an isolated repository or
  their contract explicitly says otherwise.
- If a role fails or cannot run, the Orchestrator may absorb it only when safe,
  must follow its guide, and must report the substitution and reduced
  independence.

## Runtime adapters

The Markdown role guide is the semantic source of truth. Runtime-specific files
under .claude/, .codex/, or another adapter directory should contain only the
metadata and tool/model declarations that runtime needs.

- Keep policy in AGENTS.md and role behavior in .agents/.
- Prefer references or generated adapters over independent policy copies.
- When duplication is unavoidable, update and test every adapter in the same
  change.
- Check currently available models before routing. Use Fast for mechanical
  audits, Balanced for routine research/writing/implementation, and Powerful
  only for high-stakes reasoning, adversarial exit gates, or after a failed
  Balanced attempt.

## Customization checklist

- [ ] Replace every [CUSTOMIZE] placeholder.
- [ ] Delete roles and optional sections the project does not use.
- [ ] Name exact input and output paths.
- [ ] Define the role's checkpoint unit.
- [ ] Fill the may-read, may-write, and must-not-write boundaries.
- [ ] Define prerequisite and completion gates.
- [ ] Add project-specific privacy and external-action restrictions.
- [ ] Add the real validation commands or evidence requirements.
- [ ] Define escalation triggers and the human decision owner.
- [ ] Confirm runtime adapters remain semantically aligned.
