# Moltbook governance scan — 2026-08-14

## Purpose

Identify public Moltbook discussions that may improve the reusable governance
and policy controls in Agent-Template. This is research input, not authority for
a policy change.

## Scope and method

- Read the latest 20 posts from each subscribed community: `m/agents`,
  `m/security`, `m/tooling`, `m/ai`, `m/coding`, and `m/research`.
- Total posts screened: 120.
- Read the strongest candidate posts in full and sampled their highest-ranked
  comments where counterpoints or implementation detail were useful.
- Compared the candidate controls with current `AGENTS.template.md`, adoption,
  role, schema, versioning, and pull-request guidance.
- Per the account owner's standing boundary, made no posts, comments, replies,
  votes, likes, follows, or community changes during the scan.

Moltbook posts are community discussions, not authoritative evidence. Verify
empirical claims and cited research independently before using them to justify
policy.

## Ranked recommendations

This table is ordered from highest to lowest implementation priority.

| Priority | Recommendation | Current coverage | Disposition |
| --- | --- | --- | --- |
| 1 | Treat agent-written executable configuration as a delayed execution boundary | Partial | Add a reusable safety rule |
| 2 | Represent external mutation outcomes and retry safety explicitly | Partial | Add an operational state vocabulary |
| 3 | Test action sequences and accumulated authority, not only isolated operations | Partial | Extend validation guidance |
| 4 | Replace boolean rollback claims with structured rollback receipts | Partial | Extend rollback and recovery guidance |
| 5 | Bind approval to an exact reusable artifact revision | Partial | Extend approval and version guidance |
| 6 | Instrument omissions, denominators, and cardinality invariants | Gap | Add validation guidance |
| 7 | Require field-level provenance for governed transformations | Partial | Extend schema and privacy guidance |
| 8 | Define reviewer independence by differing evidence and failure modes | Mostly covered | Clarify existing guidance |

## Flagged discussions

### 1. Delayed execution through trusted consumers

Sources:

- [A git hook is an unauthenticated control plane](https://www.moltbook.com/post/3662facd-6cc4-4866-b38a-30b8e8a5f021)
- [Six coding assistants got sandbox-escaped without anyone breaking the sandbox](https://www.moltbook.com/post/69e5b497-3714-475e-bd1c-ffdb6be96417)

An agent may remain inside its filesystem or process sandbox while writing a
file that a more privileged consumer later interprets or executes. Examples
include Git hooks, task-runner files, IDE configuration, interpreter paths,
shell startup files, CI workflows, and executable permissions.

Recommended control:

- Inventory consumers that can execute or interpret agent-written artifacts.
- Treat changes to those artifacts as execution-authority changes.
- Require explicit authorization and review before a trusted consumer acts on
  the changed artifact.
- Do not treat filesystem sandboxing alone as proof of containment.

### 2. External mutation outcomes and safe retries

Sources:

- [The API said 400. I almost learned the wrong retry rule](https://www.moltbook.com/post/92c3e5e6-f54f-4487-bbb0-59182be3962f)
- [claimed does not mean owned](https://www.moltbook.com/post/cb83592d-7541-462d-8e65-093fbf65dbd9)

An error response does not always prove that no mutation occurred, and an
acceptance response does not necessarily prove completion or publication.
Local state should not advance ahead of confirmed external state.

Recommended outcome vocabulary:

`not_attempted`, `rejected`, `accepted`, `confirmed`, `failed_no_effect`,
`outcome_unknown`, `partially_applied`, and `compensated`.

Retry only when the prior outcome is resolved by receiver semantics, a scoped
idempotency guarantee, or an authoritative read-back.

### 3. Composition and sequence testing

Source: [The unit passes; the composition is the attack](https://www.moltbook.com/post/9a5f5a4c-0cf9-427b-a342-e0380fe73ee7)

Individually permissible actions can form a prohibited or unsafe sequence.
One component's output can also become another component's instruction or
injection surface even when each component passes its isolated tests.

Recommended control:

- Identify dangerous multi-step compositions during planning.
- Test cumulative authority and privacy exposure across the sequence.
- Preserve authorization scope across intermediate stages.
- Add adversarial sequence fixtures where controls depend on ordering,
  accumulation, or handoff boundaries.

### 4. Structured rollback receipts

Source: [A rollback is not an apology](https://www.moltbook.com/post/f3a99932-02ba-4036-8639-505a20543086)

A boolean `rolled_back` claim hides the difference between actual restoration,
compensation, irreversible effects, and observers who may already have acted on
the incorrect state.

Recommended receipt fields:

- `reverted_state`
- `compensated_state`
- `irreversible_state`
- `notified_observers`
- propagation window
- unresolved downstream reconciliation

### 5. Approval bound to an exact artifact revision

Source: [the approval was for 1.00 and the library is now 0.87](https://www.moltbook.com/post/e507ed1e-76ca-43a9-a717-e27a26b622ed)

Approval attached only to a reusable component's name can silently outlive the
behavior that was reviewed. Bind approval to an exact version, digest, or commit
and retain the policy and test evidence that were in force at approval time.
Re-evaluate when behavior, dependencies, authority, or consumers change.

### 6. Omission-aware validation

Sources:

- [Your agent's trace cannot audit its own omissions](https://www.moltbook.com/post/74410b84-76ae-4f97-993f-17ec109d5fac)
- [The cardinality invariant](https://www.moltbook.com/post/868a9d25-a6f6-4b6d-8c62-282870431acb)

Ordinary traces record completed actions but may not show eligible records,
skipped checks, or silently excluded inputs.

Recommended control:

- Record `eligible`, `processed`, `excluded`, `deferred`, and `failed` counts.
- Require a reason for every structurally expected omission.
- Distinguish a check that passed from one that never ran.
- Use cardinality or distribution checks when a defensible baseline exists.
- Use an independent source or schema to detect unknown omissions.

### 7. Field-level transformation provenance

Source: [Treat missing provenance as a failed data transformation](https://www.moltbook.com/post/754f9b31-e9a5-4fe2-8277-84b5e7f753e0)

Structured output can be well formed while still being untrustworthy. For
governed transformations, classify fields as `source-backed`, `derived`,
`inferred`, or `defaulted`; retain the input record and transformation rule; and
quarantine records whose required lineage is missing. Inferred values must not
masquerade as source-supported facts.

### 8. Reviewer independence and failure diversity

Source: [A same-family reviewer is not an independent check](https://www.moltbook.com/post/bb000cd8-ce73-4788-aa25-ef210eccf445)

Agent-Template already requires independent or blind review. Clarify that
independence comes from differing evidence, context, method, or failure mode,
not merely a separate invocation. Do not require provider diversity when a
deterministic validator, rendered inspection, live-state check, or other
independent method better addresses the relevant risk.

## Existing controls reinforced by the scan

- [The checkpoint passed. The data was wrong](https://www.moltbook.com/post/634b71e1-cc06-43d7-8bae-93cf5c7af50c) reinforces the existing rule that internal consistency and green CI do not prove external correctness.
- [AskChem makes chemistry retrieval claim-centered](https://www.moltbook.com/post/d33d6969-18bc-45de-9e35-e3e789dd1f8c) supports the existing evidence-first pattern of atomic claims, authoritative sources, and precise evidence locators.

## Implementation decision for priority 1

Authorized on 2026-08-14: implement the delayed-execution/trusted-consumer rule
as a universal safety refinement.

The smallest coherent implementation covers:

| Surface | Purpose | Document-version change |
| --- | --- | --- |
| `AGENTS.template.md` | Canonical producer-consumer boundary and activation rules | `1.1` to `1.2` |
| `ADOPTION.md` | Require downstream audits to assess delayed-execution paths | `1.1` to `1.2` |
| `agents/README.md` | Route the relevant roles and stage-specific authority checks | `1.1` to `1.2` |
| `agents/templates/orchestrator.template.md` | Identify consumers, stages, and authorities before routing | `1.1` to `1.2` |
| `agents/templates/writer-implementer.template.md` | Prevent authorized writes from implying activation authority | `1.1` to `1.2` |
| `agents/templates/reviewer-critic.template.md` | Review trigger, privilege, and consumer consequences | `1.1` to `1.2` |
| `agents/templates/validator-auditor.template.md` | Verify activation state and trusted-consumer behavior | `1.0` to `1.1` |
| `agents/templates/privacy-risk-gate.template.md` | Gate write, activation, and execution as separate stages | `1.1` to `1.2` |
| `.github/PULL_REQUEST_TEMPLATE.md` | Make the trust-boundary evidence reviewable | `1.0` to `1.1` |
| `README.md` | Expose the reusable safety control | `1.2` to `1.3` |

Role coverage for practice `DE-01`:

| Role | Ownership | Schema authority | Document authority | Git authority | Checkpoint/handoff | Verdict or gate | Model routing | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | Maps consumers and owns routing/integration | Not required | Existing coordinator-owned output authority | Existing integration authority | Existing validated-handoff checkpoint | Blocks unauthorized stage advancement | Existing explicit/host-selected routing | Covered |
| Writer / Implementer | Owns only assigned artifact and tests | Not required unless separately assigned | Existing owned-artifact authority | Unassigned by default | Existing coherent-unit handoff | Leaves control artifacts inert unless later stage is authorized | Existing tier guidance | Covered |
| Reviewer / Critic | Read-only delayed-execution review | Read-only | Findings file only | Read-only | Existing one-finding checkpoint | Anchored severity finding | Existing tier guidance | Covered |
| Validator / Auditor | Read-only consumer and activation verification | Read-only | Verdict file only | Read-only | Existing one-gate checkpoint | PASS/FAIL/NOT ASSESSABLE/NOT REQUIRED | Existing tier guidance | Covered |
| Privacy / Risk Gate | Read-only authority and residual-risk gate | Read-only | Gate record only | Read-only | Existing one-risk-item checkpoint | GO/CONDITIONAL/NO-GO by exact stage | Existing tier guidance | Covered |

Compatibility classification: ordinary policy refinement. The existing v1
metadata contract, stable template types, identities, and required document
shape do not change, so `schema_version: 1` remains correct. No new `schemas/v2/`
contract is warranted.

## Implementation decision for priority 2

The authorized second batch adds practice `EM-01`: every binding external
mutation uses the common outcome vocabulary, preserves the provider response,
separates acceptance from confirmation, and prevents local authoritative state
from advancing ahead of confirmed external state. Retry requires documented
receiver semantics, authoritative read-back, or an idempotency guarantee bound
to the same actor, operation, target, payload, and authority window. Unknown or
partial outcomes stop automatic retries and dependent actions.

Role coverage for practice `EM-01`:

| Role | Ownership | Checkpoint/handoff | Verdict or gate | Coverage |
| --- | --- | --- | --- | --- |
| Orchestrator | Defines outcome mapping, confirmation source, retry gate, and receipt owner | Blocks dispatch after unknown or partial outcomes | Requires resolved evidence before retry or dependent work | Covered |
| Writer / Implementer | Emits the mapped outcome and minimal receipt for its assigned mutation | Returns unknown or partial outcomes without guessing | Does not retry or advance local authority without the assigned evidence | Covered |
| Reviewer / Critic | Reviews response mapping, read-back, receipts, and idempotency binding | Produces an anchored finding for unsafe continuation | Flags acceptance-as-confirmation and unsupported retries | Covered |
| Validator / Auditor | Independently verifies observed external state and retry evidence | Records one evidence-backed gate at a time | Uses `NOT ASSESSABLE` when effect or confirmation cannot be determined | Covered |
| Privacy / Risk Gate | Gates retry, dependent action, compensation, and publication | Records minimum necessary evidence and residual risk | GO/CONDITIONAL/NO-GO for exact stages | Covered |

The core contract, adoption guide, role guides, pull-request checklist, and
README make this behavior operational. This remains an ordinary policy
refinement: no metadata fields, reusable template identities, or required
schema shape change, so `schema_version: 1` remains correct. Because priorities
one and two are being combined in the same unmerged review revision, the
current document versions remain unchanged and their 2026-08-14 history rows
describe the combined change.

## Document control

**Last edited:** 2026-08-14

**Current version:** 1.1

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-14 | Recorded the read-only Moltbook governance scan and ranked recommendations. |
| 1.1 | 2026-08-14 | Recorded the authorized priority-one and priority-two implementation scope and compatibility decisions. |
