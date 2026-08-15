# Downstream Agent-Guidance Adoption

Use this guide from an existing Git repository to compare its agent instructions
with the canonical `main` branch of
[`mcleu/Agent-Template`](https://github.com/mcleu/Agent-Template). The goal is to
bring forward useful operating practices without erasing project-specific rules,
commands, privacy boundaries, domain knowledge, or established workflows.

This is a review-and-adapt process, not a file synchronization process.

## Default mode

Start in **audit-only** mode. Reading files, inspecting Git state, and writing a
durable comparison report are allowed. Do not edit `AGENTS.md`, `CLAUDE.md`, or
other project guidance until the user has requested implementation or approved
the exact proposed file changes.

If implementation is already explicitly authorized, still complete and save the
comparison report before editing the guidance files.

## Authority and conflict rules

Apply instructions in this order:

1. System, organization, legal, safety, and current user instructions.
2. The most specific local `AGENTS.md` governing the target path.
3. The local root `AGENTS.md` and other established project governance.
4. Tool-specific local adapters such as `CLAUDE.md`.
5. Portable practices proposed by `Agent-Template`.

The template never overrides a higher-authority rule. When both rules can apply,
keep the stricter privacy, safety, approval, evidence, and validation boundary.
When rules materially conflict, record the conflict and ask the user instead of
silently choosing one.

## Required result

Produce a durable audit at the path selected by local governance. For a new
repository, the recommended default is:

    agents/template-adoption.md

For an existing repository, keep its established role-guide directory—whether
`agents/`, `.agents/`, or another governed path—unless the comparison identifies
a demonstrated interoperability problem or the user chooses a migration.

The audit must identify:

- The exact template commit reviewed.
- The exact local repository, branch, and commit reviewed.
- Every portable practice considered.
- Local evidence showing whether the practice already exists.
- The adoption classification and rationale.
- Exact proposed target files and sections.
- Conflicts, decisions, risks, and validation required.
- Whether implementation was authorized and, if so, what changed.

Write the audit incrementally after each completed practice family. Do not hold
the entire comparison in chat or memory until the end.

## 1. Preflight the local repository

Before retrieving or comparing the template:

1. Read the local root `AGENTS.md` and every more-specific `AGENTS.md` governing
   files that may change.
2. Read the complete local `CLAUDE.md` files and relevant `agents/`, `.agents/`,
   `.claude/`, or equivalent role/runtime guidance one or two useful layers
   deep.
3. Inspect the current branch, worktree status, upstream, remotes, and worktrees.
4. Record the local `HEAD` commit and whether the working tree contains unrelated
   changes.
5. Identify the local canonical policy file. Do not assume the repository has
   already made `AGENTS.md` canonical.
6. Inventory common OS and editor metadata such as `.DS_Store`, `.idea/`,
   `.vscode/`, `.obsidian/`, swap files, and local workspace state. For each
   candidate, confirm whether it is intentionally tracked, should be ignored, or
   needs owner review. Do not delete or rewrite it automatically.
7. Do not disturb unrelated edits, switch a dirty worktree, or absorb changes
   whose ownership is unclear.

Suggested read-only inventory:

    rg --files \
      -g 'AGENTS.md' \
      -g 'CLAUDE.md' \
      -g 'ROBOTS.md' \
      -g 'robots.md' \
      -g 'agents/**' \
      -g '.agents/**' \
      -g '.claude/**' \
      -g '!node_modules/**' \
      -g '!vendor/**' \
      -g '!.git/**'

Exclude dependency, generated, archive, and vendored documentation unless it is
an intentional source of project policy. Record exclusions that could otherwise
be mistaken for authored guidance.

`Agent-Template` recommends visible `agents/` for new repositories. An existing
`.agents/` directory is not inherently stale or defective. Classify its retention
as `KEEP_LOCAL` when it works with local tooling and conventions. Use
`NEEDS_DECISION` when visibility is a user preference or when a rename has
meaningful migration cost. Propose a reference-complete rename only when there is
a demonstrated interoperability problem or explicit authorization; never create
two competing active role-guide directories.

## 2. Obtain an identifiable template snapshot

Compare against the current remote `main` when network access is available. Use
a temporary location outside the target repository so the comparison does not
add a submodule, nested repository, dependency, or untracked files.

Example:

    template_audit_dir="$(mktemp -d)"
    git clone --depth 1 --branch main \
      https://github.com/mcleu/Agent-Template.git \
      "$template_audit_dir/Agent-Template"
    git -C "$template_audit_dir/Agent-Template" rev-parse HEAD

Record the returned commit in the audit before comparison. If only a cached or
offline copy is available, record its path, commit, and last known date; label
the comparison as potentially stale and do not claim that it reflects current
`main`.

Do not copy files from an unidentified working tree or compare against a branch
merely because its name looks current.

## 3. Establish the local baseline

Read the local guidance in full before searching for missing language. Summarize
the existing contract by practice family and cite the exact path and section.
Include implicit project constraints expressed in scripts, tests, schemas,
branch guards, privacy checks, contribution guidance, or folder structure when
they materially affect agent behavior.

Do not treat missing wording as a missing practice if an enforceable local
mechanism already supplies the behavior. Conversely, do not mark a practice as
present merely because a similarly named heading exists.

Checkpoint the completed baseline in the audit before evaluating changes.

## 4. Compare practice families

Review the template by concept, not by line-by-line copying. At minimum, assess
these practice families:

| Practice family | Questions to answer |
| --- | --- |
| Instruction hierarchy | Is the canonical policy file clear? Do nested rules have defined scope and precedence? |
| Session and Git workflow | Are preflight, trunk, feature-branch, commit, push, PR, CI, and no-agent-merge rules explicit and accurate? |
| Git authority and traceability | Is it explicit who may branch, stage, commit, push, open a PR, tag, release, or merge? Can a change be traced from decision through reviewed revision and release? |
| Checkpointing and resume | Is each natural unit written durably? Can interrupted work resume from the first unfinished unit? |
| Folder and artifact ownership | Are source, work state, research, templates, generated output, private data, and archives separated? Does each artifact have one writer? |
| Evidence and research | Are sources, URLs, check dates, confidence, assumptions, unknowns, and source-of-truth precedence preserved? |
| Privacy and publication | Are private inputs, public output, synthetic examples, secret/PII scans, approval gates, and publication surfaces defined? |
| Planning and ambiguity | Are prerequisite gates, decision owners, approval boundaries, reversibility, and one-question-at-a-time escalation clear? |
| Multi-agent operation | Are roles bounded by exact reads/writes, checkpoints, handoffs, host-selected or explicit model routing, and serialized overlapping writes? |
| Schemas and versioning | Are human-readable domain meaning and versioned producer/consumer invariants assigned clear, complementary authorities? Are schema contracts kept in version directories with stable IDs, integer versions, introduction evidence, owners, compatibility, migrations, fixtures, and bump authority? Does every reusable template declare its schema version and stable type? Do new or materially revised durable human-authored files have a document version, last-edited date, and append-only history without invented legacy history? Are document, schema, release, migration, and Git revisions kept distinct? |
| Review and validation | Are review independence, anchored findings, binary verdicts, actual-artifact checks, visual QA, and stale-check invalidation covered? |
| High-risk filesystem work | Are audit-first plans, exact mappings, collision refusal, provenance, approval binding, sole-writer execution, rollback, and independent verification required where relevant? |
| Delayed execution and trusted consumers | Can an agent-written hook, workflow, task, startup file, plugin setting, interpreter path, permission, or other control artifact later be executed or interpreted by a more privileged consumer? Are writing, activation, and execution separate authorities with known triggers and rollback? |
| External mutation outcomes and retries | Does each binding external action distinguish attempted, accepted, confirmed, failed-with-no-effect, unknown, partial, and compensated outcomes? Are retries gated by receiver semantics, scoped idempotency, or authoritative read-back? |
| Composition and sequence safety | Can individually permitted steps accumulate prohibited authority or data exposure? Are authorization and provenance preserved at each boundary, and are order, replay, omission, duplication, and partial-failure paths tested? |
| Rollback and compensation evidence | Does rollback distinguish verified restoration, compensation, irreversible effects, propagation, notified observers, and unresolved downstream reconciliation instead of relying on a boolean claim? |
| Revision-bound approval | Is each material approval bound to an immutable artifact revision plus the reviewed policy/test evidence, scope, stages, target, and invalidation triggers? |
| Omission-aware validation | Is the eligible population independently defined and reconciled to processed, excluded, deferred, and failed outcomes? Are skipped checks distinct from passes and cardinality/distribution shifts investigated? |
| Field-level transformation provenance | Are governed output fields classified as source-backed, derived, inferred, or defaulted with source/rule revisions, preserved lineage for consumers, and quarantine when required lineage is missing? |
| Reviewer independence and failure diversity | Is each independent gate designed around a material failure mode and a genuinely different evidence/method path? Are shared context and blind spots disclosed rather than treating separate invocations or provider diversity as sufficient? |
| Documentation improvement | Are decisions, assumptions, risks, retrospectives, schemas, and generated-versus-source distinctions durable? |
| Completion and handoff | Must the agent report files, commit, PR/CI state, checks, explicit unknowns, open gates, and the next action? |

For each family, compare `AGENTS.template.md`, `ADOPTION.md`, and only the role
templates relevant to the downstream project. Do not import every optional role
or high-risk procedure into a simple repository.

## 5. Classify each candidate practice

Use one of these states:

| State | Meaning |
| --- | --- |
| `PRESENT` | The local repository already implements the practice effectively |
| `ADOPT` | The template language fits and can be added with little or no change |
| `ADAPT` | The practice is useful but must be rewritten for local paths, commands, risks, or ownership |
| `KEEP_LOCAL` | A local rule is clearer, stricter, or better suited to the project |
| `NEEDS_DECISION` | The choice changes authority, workflow, privacy, architecture, or another material outcome |
| `NOT_APPLICABLE` | The practice does not fit this repository; record why |
| `REJECT` | The template practice would weaken, conflict with, or misrepresent the local contract |

Never copy `[CUSTOMIZE]`, example paths, model names, commands, branch names, or
optional modules without resolving them against the actual repository.

Use a matrix like this in the selected audit file:

| ID | Practice | Template evidence | Local evidence | State | Proposed target | Rationale / risk |
| --- | --- | --- | --- | --- | --- | --- |
| GIT-01 | Pull trunk before editing | `AGENTS.template.md` section ... | `AGENTS.md` section ... | `ADAPT` | `AGENTS.md` Git workflow | Local trunk is ... |

Assign stable IDs so findings, decisions, edits, and validation evidence can
reference the same item.

## 6. Prepare the adoption plan

After the matrix is complete:

1. Group accepted items by target file and section.
2. Draft exact proposed wording or a precise edit description.
3. Identify local language that will be retained, replaced, or moved.
4. List commands, paths, links, and branch rules that require live verification.
5. List any privacy, publication, destructive-action, or external-action gate.
6. For every executable or interpreted control artifact in scope, list its
   producer, consumers, privilege boundary, discovery/loading rule, activation
   trigger, current state, separately authorized stages, and rollback or disable
   path.
7. For every external mutation in scope, define its outcome-state mapping,
   confirmation source, idempotency scope, receipt location, retry gate, and
   behavior for unknown or partial outcomes.
8. For every materially risky multi-step workflow, map actors, inputs, outputs,
   authority, data exposure, external effects, checkpoints, and consumers;
   define sequence invariants and adversarial test cases.
9. For every material rollback or compensation path, define the receipt fields,
   downstream observers/consumers, propagation window, verification source,
   reconciliation owner, and residual irreversible state.
10. For every reusable or high-impact approved artifact/action, define its
    immutable revision identity, approval record, exact scope/stages, governing
    policy and evidence revisions, expiry, and material-change invalidators.
11. For every workflow where silent omission is material, define the independent
    eligible population, mutually exclusive outcome categories, reconciliation
    invariant, omission reasons/owners, and cardinality/distribution baselines.
12. For every governed transformation, identify lineage-required fields,
    classification vocabulary, source locator and transformation-rule versions,
    downstream retention, privacy constraints, and quarantine behavior.
13. For every independent review gate, name the claim/failure mode, producer
    blind spot, independent evidence/method, shared dependencies/context, and
    residual risk when the failure cannot be independently observed.
14. Separate straightforward `ADOPT`/`ADAPT` work from `NEEDS_DECISION` items.
15. State the smallest coherent implementation batch.

For a lightweight existing repository, consider the **smallest useful
adoption** profile first:

- expand the canonical operating contract only where the audit finds a gap;
- retain one thin runtime adapter when the host needs one;
- keep the adoption audit and a locally appropriate `VERSIONING.md`;
- add only the schema contracts relevant to active shared interfaces;
- use the pull-request checklist and the repository's native tests; and
- omit generic roles, a second validation stack, and repository-wide metadata
  when they do not address an evidenced risk.

Expand beyond this profile only when the audit identifies distinct ownership,
handoff, validation, privacy, or compatibility needs.

### Require role-guide coverage

Do not treat a root `AGENTS.md` change as automatically adopted by sub-agents.
For every accepted practice that affects multi-agent behavior, identify each
relevant role and confirm that its own guide makes the behavior operational.

Add a role-coverage table to the audit:

| Practice ID | Role | Guide path | Ownership | Schema authority | Document-version authority | Git authority | Checkpoint | Handoff | Verdict/gate | Model tier | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ID] | [role] | [path] | explicit/missing | explicit/missing/not-required | explicit/missing/not-required | explicit/missing/not-required | explicit/missing | explicit/missing | explicit/missing/not-required | explicit/host-selected/not-required/missing | covered/gap/not-required |

- `covered` requires explicit ownership, checkpointing, handoff, applicable
  schema, document-version, and Git authority when applicable, verdict/gate
  semantics, and an explicit model tier or an intentional `host-selected` or
  `not-required` routing decision with rationale in the role guide itself.
- Use `not-required` only when the practice or field genuinely does not apply to
  that role, and record why.
- A missing or implicit field is a `gap`, not inherited coverage.
- Include affected role-guide edits in the implementation batch or defer the
  practice explicitly. Do not declare adoption complete while relevant role
  gaps remain.

In audit-only mode, stop here and give the user the durable report path, the
recommended first batch, and one focused question if a material decision is
required. Do not quietly turn an audit into a cross-repository rewrite.

## 7. Implement an authorized adoption

When implementation is explicitly authorized:

1. Pull the repository's authoritative trunk and current working branch.
2. Create or use a correctly named feature branch; never commit directly to the
   authoritative trunk.
3. Update the canonical local policy first, normally the root `AGENTS.md`.
4. Update nested `AGENTS.md` files only when their scoped behavior changes.
5. Update every relevant role guide identified by the role-coverage table.
6. Update `CLAUDE.md` last so it points to the canonical policy and retains only
   genuinely Claude-specific runtime instructions.
7. Make the smallest coherent diff. Preserve stricter local rules and verified
   project-specific commands, paths, schemas, role names, and approval gates.
8. Keep the adoption and role-coverage matrices current as each item is
   implemented, deferred, or rejected.
9. Start or advance the document-control version for every durable audit,
   guidance file, or role guide materially changed in the batch. Update its
   last-edited date and append one specific history row.
10. Perform only the separately authorized Git stages. Treat local branch
    creation, commit, push, draft pull request, ready-for-review transition,
    merge, and release as distinct authorities. A remote's existence does not
    authorize an external action. Never merge unless the owner explicitly
    grants that authority.

Do not replace a mature local `AGENTS.md` wholesale with the template. Merge
practices into the existing structure unless the user explicitly approves a
larger migration and the review demonstrates that it preserves all local
behavior.

### `CLAUDE.md` guidance

When no distinct Claude behavior is required, prefer a thin adapter:

    # Claude Instructions

    The canonical project operating contract is [AGENTS.md](AGENTS.md).
    Read and follow it before making changes. Keep shared policy in AGENTS.md.

When Claude-specific capabilities or restrictions are necessary, keep them in a
short, clearly labeled runtime section after the canonical pointer. Do not copy
the full `AGENTS.md` into `CLAUDE.md`; duplicated policy will drift.

If the local repository currently treats `CLAUDE.md` as canonical, record that
fact and propose the migration separately. Do not reverse authority merely to
match the template.

### Close the audit without self-reference

Do not require an audit file to contain the commit or CI result of the commit
that contains that same metadata.

When commit-level traceability is required:

1. Create the implementation commit containing the approved policy and role
   changes.
2. Observe the checks for that implementation commit.
3. Create one audit-closure commit that records the implementation commit and
   its observed CI/check state in the durable audit.
4. Report the audit-closure commit and its own CI/check state in the task handoff
   or pull request. Do not amend the audit again merely to record its closure
   commit; that would recreate the loop.

If local policy allows the audit and implementation to share one commit, record
the base commit and final diff in the audit, then report the resulting commit and
CI externally in the handoff.

## 8. Validate the adopted guidance

After the final edit:

- Re-read every changed guidance file in full.
- Confirm instruction hierarchy and path scope remain unambiguous.
- Search for unresolved placeholders, example-only values, obsolete model IDs,
  stale branch names, broken links, nonexistent commands, and invalid paths.
- Check that no local privacy, safety, evidence, approval, or domain rule was
  weakened or dropped.
- Confirm agent-written control artifacts remain inactive unless activation was
  separately authorized, and validate the actual trusted consumer rather than
  only the artifact's syntax or location.
- Confirm external mutations do not advance local authoritative state before
  confirmation; acceptance remains distinct from completion, and no unknown or
  partial attempt is retried without receiver semantics, scoped idempotency, or
  authoritative read-back.
- Confirm high-risk workflows were evaluated end to end, authorization and
  provenance survive every boundary, cumulative authority/data exposure remain
  within scope, and order/replay/duplicate/omission/partial-failure cases have
  evidence or a named `NOT ASSESSABLE` result.
- Confirm rollback claims identify verified reverted state separately from
  compensation and irreversible effects, account for observers and propagation,
  and leave unresolved downstream reconciliation explicitly open.
- Confirm material approvals resolve to the exact artifact, policy, and evidence
  revisions reviewed and are invalidated after relevant behavior, dependency,
  authority, consumer, target, environment, or control changes.
- Confirm applicable eligible populations reconcile to processed, excluded,
  deferred, and failed outcomes; skipped checks are not passes; omissions have
  reasons; and independent inventories or baselines expose unknown exclusions.
- Confirm governed fields retain source/rule lineage and the source-backed,
  derived, inferred, or defaulted distinction through consumers; required
  missing lineage is quarantined and lineage metadata respects privacy rules.
- Confirm independent review gates target named failure modes with evidence or
  methods not derived solely from the producer; shared context and blind spots
  are disclosed, and unobservable failures are `NOT ASSESSABLE`.
- Check `AGENTS.md` and `CLAUDE.md` for duplicated or contradictory policy.
- Confirm the role-coverage table has no unexplained gaps for accepted
  multi-agent practices.
- Confirm each affected schema has one authority, stable ID/version, verified
  producers/consumers, compatibility classification, migration path when
  required, and an authorized bump owner.
- Confirm every new or changed reusable template declares the schema version,
  stable type/identity, document version/last-edited date, and any role-specific
  metadata required by its versioned contract. Do not infer legacy status from
  missing metadata alone.
- Confirm every new or materially changed durable human-authored file has one
  current document version, a matching last-edited date/history row, and no
  reused or silently rewritten version entry.
- Confirm document, schema, product/release, deliverable, migration/manifest,
  and Git revision identifiers are not conflated.
- Verify trunk, deployment target, hosting/runtime, CI, and release claims
  against actual remotes, workflow files, deployment configuration, and other
  authoritative project files. Names and prior prose are not sufficient proof.
- Treat search, lint, link, case, secret, and other scanner matches as
  candidates. Check each candidate against the authoritative file, path
  semantics, and documented approved exceptions before marking it a failure.
- Record candidate disposition as confirmed defect, approved exception, false
  positive, or unresolved. An unresolved required candidate prevents a pass.
- Run documentation lint, link checks, policy tests, branch guards, and privacy
  checks that the local repository provides.
- Run `git diff --check`, inspect the complete diff, stage exact files, and
  inspect the staged diff before committing.
- Record every check with `PASS`, `FAIL`, `NOT ASSESSABLE`, or `NOT REQUIRED`.
  Use `NOT ASSESSABLE` only when a required gate cannot be evaluated. Use
  `NOT REQUIRED` only when the gate is outside the approved change scope, with a
  reason. A skipped required check is not a pass.
- Record the implementation commit and its observed CI/check state in the audit
  through the closure procedure above. Report the audit-closure commit, branch,
  pull request, and final CI state in the handoff or PR rather than recursively
  editing the audit.

An independent Reviewer or Validator is appropriate when the adoption changes
privacy, destructive-action, publication, regulated, production, or other
high-stakes controls.

## Handoff format

Return a concise, evidence-backed summary:

    TEMPLATE | repo=mcleu/Agent-Template | branch=main | commit=<sha> | checked=<date>
    LOCAL | repo=<path or URL> | branch=<branch> | base-commit=<sha>
    AUDIT | path=<durable comparison report>
    RESULT | present=<n> | adopt=<n> | adapt=<n> | keep-local=<n> | decision=<n> | not-applicable=<n> | reject=<n>
    IMPLEMENTATION | commit=<sha> | ci=<observed state>
    AUDIT-CLOSURE | commit=<sha or none> | ci=<observed state or pending>
    CHANGE | <path> | <implemented or proposed practice IDs>
    DOCUMENT | path=<path> | version=<MAJOR.MINOR> | change=<history summary>
    CHECK | <name> | pass | fail | not-assessable | not-required | <evidence or reason>
    OPEN | <decision, risk, approval, unknown, or none>
    NEXT | <smallest safe next action>

Do not say the repository is aligned merely because files were copied or the
diff is empty. Alignment requires practice-level evidence and a clean validation
result.

## Ready-to-use instruction for a future agent

    Compare this repository's authored AGENTS.md, CLAUDE.md, and relevant
    agents/, .agents/, and .claude/ guidance against the current main
    branch of https://github.com/mcleu/Agent-Template using ADOPTION.md from that
    repository. Start audit-only. Read the local rules in full, identify the
    exact template and local commits, and write the practice-by-practice matrix
    incrementally to the repository's locally governed role-guide directory.
    Preserve stricter and project-specific rules. Add a role-coverage table for
    every accepted multi-agent practice. Do not edit guidance until the
    comparison and proposed first batch are durable and I have authorized
    implementation. If implementation is authorized, use a feature branch,
    make minimal changes to canonical AGENTS.md first, relevant role guides
    next, and CLAUDE.md last. Validate reality claims and scanner candidates,
    apply document control to new and materially revised durable authored files,
    baseline untouched legacy files without invented history, close commit
    metadata without self-reference, and perform only the separately authorized
    branch, commit, push, or PR stages. Never merge without explicit authority.

## Document control

**Last edited:** 2026-08-14

**Current version:** 1.2

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Added audit-first adoption, role coverage, reality checks, and document-version adoption. |
| 1.1 | 2026-08-08 | Added lightweight adoption, host-selected routing, gradual legacy document control, and stage-specific publication authority. |
| 1.2 | 2026-08-14 | Added adoption coverage for all eight ranked controls, including failure-diverse review. |
