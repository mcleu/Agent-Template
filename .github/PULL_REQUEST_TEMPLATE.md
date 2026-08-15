<!--
schema_version: 1
type: pull_request
template_id: pull-request
document_version: "1.1"
last_edited: "2026-08-14"
-->

## Outcome and scope

- Outcome:
- In scope:
- Out of scope:
- Source requirement, issue, or decision:

## Schema and version impact

Delete rows that do not apply. Use `NOT REQUIRED` with a reason instead of
leaving an applicable surface ambiguous.

| Surface | Current | Proposed | Authority/owner | Compatibility and rationale |
| --- | --- | --- | --- | --- |
| Product/package release | | | | |
| Schema/interface | | | | |
| Durable document content | | | document owner | history preserved |
| Human deliverable | | | | |
| Migration/manifest | | | | |
| Git source revision | | | | immutable traceability only |

- Canonical schema(s):
- Template/record `schema_version` and stable `type`:
- Durable documents and current `document_version` values:
- Introduction marker or legacy baseline:
- Producers/consumers changed:
- Migration, cutover, support window, and rollback/stop plan:
- Generated representations and drift check:

## Validation

- [ ] Required schema and version decisions are reflected in authoritative
      files.
- [ ] Every new or changed reusable template/structured artifact declares the
      schema version, document version/date, type, and identity required by its
      versioned schema and document-control contracts.
- [ ] Every new or materially changed durable human-authored file has a matching
      current document version, last-edited date, and append-only history row.
- [ ] Producers, consumers, fixtures, tests, migrations, examples, and
      documentation are aligned or explicitly gated.
- [ ] Synthetic fixtures cover old/new and missing/unknown/invalid behavior as
      applicable.
- [ ] Relevant format, lint, type, unit, contract, integration, build, privacy,
      visual, and branch checks ran or have a named verdict and reason.
- [ ] Scanner candidates were adjudicated against authoritative files and
      approved exceptions.
- [ ] Executable or interpreted control artifacts identify their consumers,
      triggers, privilege boundaries, activation state, and rollback/disable
      path; no stage exceeds its separate authority.
- [ ] External mutations distinguish acceptance from confirmation, preserve a
      minimal receipt, and retry only after authoritative read-back, documented
      receiver semantics, or correctly scoped idempotency evidence.
- [ ] Material multi-step workflows have an end-to-end sequence map and
      adversarial evidence for applicable reorder, replay, duplicate, omission,
      stale-input, partial-failure, and instruction/data-confusion paths.
- [ ] Rollback/compensation evidence separates reverted, compensated, and
      irreversible state and accounts for observers, propagation, verification,
      and unresolved downstream reconciliation.
- [ ] Material approval identifies the immutable artifact revision, approved
      scope/stages/target, governing policy and evidence revisions, expiry, and
      material-change invalidators; the actual revision was resolved.
- [ ] The final diff contains no private, generated, unrelated, or unintended
      files.

Checks and evidence:

```text
<command or inspection> | PASS | FAIL | NOT ASSESSABLE | NOT REQUIRED | <evidence/reason>
```

## Git and release state

- Branch:
- Implementation commit:
- Observed CI/check state:
- Release/tag/deployment action prepared, if any:
- Human approval still required for:

- [ ] Changes are on a feature branch and commits are logically scoped.
- [ ] Trunk, remote, workflow, deployment, and release claims were checked
      against actual configuration/state.
- [ ] No tag was moved and no shared history was rewritten.
- [ ] This pull request has not been merged or auto-merged by an agent.

## Risks, approvals, and unknowns

- Privacy/security/safety impact:
- Delayed-execution/control artifacts changed:
- Trusted consumers, loading rule, trigger, and privilege boundary:
- Authorized stage: draft/write/install/activate/execute/deploy/NOT REQUIRED
- External mutation outcome/confirmation source: NOT REQUIRED
- Idempotency scope or retry gate: NOT REQUIRED
- Mutation receipt and residual uncertainty: NOT REQUIRED
- Sequence map and cumulative authority/privacy invariants: NOT REQUIRED
- Adversarial sequence evidence or `NOT ASSESSABLE` reason: NOT REQUIRED
- Recovery receipt/reverted, compensated, and irreversible state: NOT REQUIRED
- Observers, propagation, and unresolved reconciliation: NOT REQUIRED
- Approval record and exact artifact revision: NOT REQUIRED
- Approved policy/evidence revisions, scope, expiry, invalidators: NOT REQUIRED
- Approval gates:
- Remaining unknowns:
- Rollback or recovery path:

<!--
## Document control

Last edited: 2026-08-14
Current version: 1.1

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the controlled pull-request template. |
| 1.1 | 2026-08-14 | Added review evidence for delayed execution, mutations, sequences, recovery, and revision-bound approval. |
-->
