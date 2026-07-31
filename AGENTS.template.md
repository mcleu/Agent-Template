# AGENTS.md Template — Project Operating Contract

> Copy this file to the repository root as AGENTS.md. Replace every
> [CUSTOMIZE] placeholder, remove optional sections that do not apply, and keep
> project-specific facts out of generic runtime adapters.

## 0. How to use this contract

- AGENTS.md is the canonical, tool-neutral operating contract for this project.
- Human instructions in the current task override this file. More-specific
  AGENTS.md files may add rules for their own subdirectories.
- Tool-specific entry files such as CLAUDE.md should point here instead of
  duplicating these rules. Update the canonical contract and adapters in the
  same change when runtime metadata must stay aligned.
- README.md explains the project to users. AGENTS.md governs how humans and
  agents work in the repository. Do not make either file carry both jobs.
- Remove examples and optional clauses that do not fit this project. A shorter,
  accurate contract is safer than a comprehensive contract nobody follows.
- If this contract conflicts with the actual repository, stop, report the
  conflict, and propose a contract update. Do not silently follow undocumented
  reality.

Suggested CLAUDE.md:

    # Compatibility pointer

    The repository's canonical operating instructions are in
    [AGENTS.md](AGENTS.md). Read and follow that file. Keep project rules there
    rather than maintaining a tool-specific copy.

## 1. Project identity and boundaries

### Purpose

- Project: [CUSTOMIZE: name]
- Outcome: [CUSTOMIZE: one sentence describing what this project produces]
- Primary users: [CUSTOMIZE]
- Source of truth: [CUSTOMIZE: file, database, controlled system, or external
  record that wins when sources disagree]
- This repository is: [CUSTOMIZE: software / framework / document library /
  knowledge base / mixed]
- This repository is not: [CUSTOMIZE: common category error, such as a QMS,
  legal opinion, private-record vault, production database, or final authority]

### Scope

- In scope: [CUSTOMIZE]
- Out of scope: [CUSTOMIZE]
- High-risk surfaces: [CUSTOMIZE: privacy, money, health, legal, regulated
  product, external communications, destructive file operations, production]
- Actions requiring explicit human approval: [CUSTOMIZE]
- Files or directories that must never be changed: [CUSTOMIZE]

### Authority order

When instructions or facts conflict, use this precedence:

1. Current explicit user instruction.
2. The most specific AGENTS.md covering the target path.
3. This root AGENTS.md.
4. Project schemas, contracts, decision logs, and authoritative records.
5. README files and other explanatory documentation.
6. Existing implementation and historical notes.

Do not treat generated output, summaries, stale plans, or model memory as a
current source of truth. Verify drift-prone facts cheaply when possible.

## 2. Repository map

Keep only the directories the project needs. Separate reusable framework,
private inputs, working state, generated output, and archived history.

    AGENTS.md             Canonical operating contract
    CLAUDE.md             Thin compatibility pointer to AGENTS.md
    README.md             User-facing purpose, setup, and entry points
    src/                  Product or application source
    lib/                  Reusable libraries with stable interfaces
    tests/                Automated tests mirroring owned code surfaces
    docs/                 Durable architecture and operating documentation
    research/             Source-linked research, one topic per file
    templates/            Blank, reusable, non-sensitive starting artifacts
    examples/             Synthetic examples safe to commit and publish
    scripts/              Deterministic validation, export, and maintenance tools
    schemas/              Versioned data and interface contracts
    plans/                Reviewable implementation plans and decision records
    memory/               Optional durable local context; private by default
    .github/workflows/    CI checks that enforce repository contracts
    .agents/              Tool-neutral roles, skills, and workflows
    .claude/              Claude runtime adapters; policy remains in AGENTS.md
    .codex/               Codex runtime adapters; policy remains in AGENTS.md
    private/              Local sensitive material; ignored unless explicitly safe
    work/                 Interruptible local working state; normally ignored
    output/               Generated artifacts; normally ignored
    Archive/              Superseded material preserved with original names

### Folder rules

- [CUSTOMIZE: list each real top-level path, its purpose, and its owner.]
- Use templates to scaffold new work; do not modify the canonical blank
  template while filling a live case, trip, filing, spec, or record.
- Keep live/private workspaces separate from generic, shareable framework files.
- Use stable paths for evidence and records. Represent lifecycle state in
  metadata rather than moving files between status folders unless the schema
  explicitly requires moves.
- Do not add a new top-level directory or abstraction without showing why the
  existing structure cannot represent the work.
- Treat vendor, dependency, build, cache, and generated directories as
  non-authored material unless the task explicitly targets them.

## 3. Start-of-session protocol

Before the first write:

1. Read this file and every more-specific AGENTS.md governing the target paths.
2. Read the relevant schema, role definition, skill, README section, and source
   of truth. Do not load unrelated private context speculatively.
3. Inspect git status, the current branch/worktree, upstream, remotes, and
   unrelated changes. Preserve all pre-existing work.
4. Fetch origin. If the worktree is clean, fast-forward the working branch and
   absorb current origin/[AUTHORITATIVE_TRUNK] before editing. New branches
   start from the current authoritative trunk, which may not be named main.
5. If the tree is dirty, do not pull, rebase, stash, overwrite, or bundle the
   user's changes into your work. Determine a safe isolated branch or worktree.
6. Identify the smallest owned file set, expected output, validation commands,
   privacy boundary, and approval gates.
7. For work lasting more than one natural unit, create or update a durable plan
   and mark exactly one step in progress.

If the repository has no remote, say so. Continue with local version control,
but do not claim a push, CI run, or pull request occurred.

## 4. Working style

### Read before writing

- Inspect the current implementation and nearby conventions before proposing a
  change.
- Read the complete source before classifying, reorganizing, or rewriting it.
  Titles, filenames, headings, and first paragraphs are weak evidence and may be
  stale or incomplete.
- Search broadly enough to identify every producer, consumer, schema, test, and
  documentation reference affected by a shared field or interface.
- Prefer the smallest task-scoped context packet. Specialists should request a
  missing source rather than reading every private file by default.
- Separate confirmed evidence, sourced claims, inferences, assumptions,
  recollections, and unknowns. Never turn an inference into a settled fact.
- Do not invent data, metrics, citations, technical details, authorship,
  intent, or outcomes.

### Write as you go

- Never hold a multi-unit deliverable in memory until the end.
- Write each completed natural unit to its assigned file before starting the
  next: one requirement, finding, research question, section, record, or
  cross-file update.
- A checkpoint is the actual durable artifact, not a progress summary in chat.
- On resume, read the existing artifact and continue from the first unfinished
  unit. Do not recreate completed evidence from memory.
- Commit at logical milestones; file checkpoints should be more frequent than
  commits.

### Scope and change discipline

- Touch as few files as possible. Do not refactor, reformat, rename, reorganize,
  or upgrade dependencies unless required by the requested outcome.
- Preserve voice, intent, factual specificity, file formats, and unrelated
  working-tree changes.
- Follow existing naming and date conventions. [CUSTOMIZE: project naming rule]
- Keep edits reviewable. Explain what changed, why, and any risk introduced.
- When the safe default is unclear, do less and report more.

### Decisions and questions

- Pause before major scope, architecture, privacy, destructive-operation, or
  publication decisions and confirm continued alignment.
- Resolve what can be resolved from authoritative local evidence first.
- When user input is necessary, ask one focused question and wait. Include a
  recommended default and the consequence of choosing it.
- Never advance past an unanswered blocking question.
- Ambiguity should not block independent, unambiguous read-only work.

## 5. Research and evidence

- Before external lookup, assign the durable file research/<topic>.md or the
  project-specific equivalent.
- Write research piece by piece. After each completed source or question, record
  the finding, direct source URL or citation, publication date when relevant,
  date checked, and remaining uncertainty.
- Prefer official primary sources. Use secondary sources only when they add
  necessary analysis or when primary evidence is unavailable, and label that
  limitation.
- Verify current branches, CI, bookings, prices, laws, schedules, product
  details, and other drift-prone facts live when they affect the result.
- Preserve originals as evidence. Add source-linked summaries, actions,
  questions, or hubs as derived layers instead of rewriting source material.
- Do not reuse research whose governing facts have changed. Reconfirm the
  premise before applying earlier work.
- When retrieval is blocked after a materially different retry, report what was
  verified locally and ask for the missing source rather than fabricating a
  workaround.

Recommended research file:

    # [Topic]

    - Status: in progress | complete | blocked
    - Scope:
    - Questions:
    - Checked:

    ## Findings

    ### [Completed unit]
    - Finding:
    - Evidence:
    - Source:
    - Date checked:
    - Confidence:
    - Remaining uncertainty:

    ## Decisions

    ## Unfinished work

## 6. Privacy, confidentiality, and publication

### Repository boundary

- Declare whether this repository is public, private, local-only, or mixed.
- Keep reusable framework code and synthetic examples separate from real
  customer, employee, patient, financial, property, travel, filing, or vendor
  material.
- Put local/private paths in .gitignore before adding sensitive files. Include a
  safe .env.example rather than real credentials or identifiers.
- Never commit API keys, account numbers, payment data, health details, home
  addresses, passport or loyalty identifiers, attorney-client work product,
  unreleased product data, confidential business terms, or third-party personal
  information.
- Do not quote confidential material in commits, pull requests, logs, reports,
  screenshots, examples, or generic instruction files. Git history should be
  treated as permanent disclosure.
- Use the minimum data required for each handoff. A downstream role does not
  automatically receive every upstream private source.

### Sensitivity model [OPTIONAL]

Use a small, machine-checkable vocabulary:

| Class | Meaning | Agent permission |
| --- | --- | --- |
| public | Cleared for the repository and its intended audience | Normal work |
| approval-required | May be used only in paraphrase and listed for owner review | Draft, then gate |
| private | Must not appear in public or remote artifacts | Existence-only or local processing |
| restricted | Legal, regulated, vendor, or specially protected material | No semantic review unless explicitly authorized |

- Fail toward restriction. An over-classified item can be reviewed; an
  under-classified item can become an irreversible disclosure.
- Keep classification in structured metadata when possible. Free-text markers
  may remain as redundant signals but should not be the only protection.
- Preserve unknown or missing classifications. Do not infer permission from the
  absence of a label.

### Privacy gate [OPTIONAL]

For work derived from private material, run the gate twice:

1. Before writing: review the proposed plan and remove blocked facts.
2. Before delivery: review the actual diff and generated artifacts.

The gate verifies provenance, sensitivity, paraphrasing requirements, third-party
privacy, containment of local working files, and an owner approval list. The
gate may block but does not silently rewrite another role's work.

### External actions

- Never send a message, submit a form, publish, make a purchase, enter payment
  details, approve a filing, deploy to production, or merge a pull request
  without the required explicit authority.
- It is acceptable to prepare or stage a reversible action up to the clearly
  defined binding boundary. Stop when that boundary is unclear.
- After a human completes an external action, capture only the minimum safe
  evidence needed by the repository.

## 7. Version control and pull requests

### Branch and worktree rules

- Always use Git for tracked changes. Every session that modifies tracked files
  ends with a commit unless the user explicitly requests an uncommitted diff.
- Never author changes directly on the authoritative trunk.
- Branch naming: feat/, fix/, docs/, chore/, filing/, apply/, trip/, or another
  documented project prefix followed by a short lower-case slug.
- Before editing an existing remote repository, update the authoritative trunk
  in its clean checkout/worktree, then update the working branch and absorb the
  current trunk according to repository policy:

    git fetch origin
    git -C [TRUNK_WORKTREE] pull origin [AUTHORITATIVE_TRUNK]
    git pull origin [CURRENT_BRANCH]
    git merge origin/[AUTHORITATIVE_TRUNK]

- Review incoming changes before writing. If the authoritative trunk is not
  main, document the real trunk and do not trust the branch name by convention.
- Use isolated worktrees for concurrent or lifecycle-specific work when branch
  contents must remain separated.
- Preserve unrelated changes. Never use reset --hard, clean, broad checkout,
  force-push, or an automatic stash as a convenience.

### Commits

- Use concise conventional prefixes such as feat:, fix:, docs:, chore:, test:,
  refactor:, or a project-specific prefix.
- Commit one logical change at a time. Do not mix human edits, generated
  outputs, sensitive local work, or unrelated cleanup into the same commit.
- Inspect git diff and git diff --staged before every commit.
- Commit messages describe the tracked change without quoting private content.
- If a local/private workspace is its own Git repository, commit there and keep
  it separate from the shareable framework repository.

### Pull requests

- Push the feature branch and open a descriptive pull request before merging to
  the authoritative trunk.
- Agents may create commits and draft pull requests but never merge, enable
  auto-merge, approve their own pull request, or mark it ready without
  authorization.
- Monitor authored pull requests for CI, conflicts, review feedback, and
  closure. Fix in-scope CI failures at their root and push to the same branch.
- When asked to address concrete review feedback, implement the selected fix,
  validate it, commit it, push it, and report the commit and checks. Do not stop
  at an acknowledgement.
- A green CI run is a handoff checkpoint, not proof that every external or
  visual behavior was verified.
- If the repository or branch intentionally has no PR/CI path, run the
  equivalent checks locally and state that limitation explicitly.

## 8. File safety, migrations, and versioned deliverables

### Ordinary edits

- Prefer append-only records for evidence, expenses, confirmations, decisions,
  corrections, and refunds. Represent a correction as a new linked event rather
  than rewriting history when auditability matters.
- Preserve stable IDs, slugs, filenames, and schema keys once referenced. Mark
  an item superseded; do not reuse or renumber its identity.
- Never overwrite source material supplied by a user. Save originals verbatim
  before producing derived analysis.
- Do not delete merely because a file appears unused. Check references,
  generated consumers, alternate tools, and archival rules.

### Versioned human deliverables [OPTIONAL]

- Working-state files may keep stable names when the workflow requires them.
- Human-facing versions use a documented pattern such as:

    YYYY-MM-DD_Project_Subject_Deliverable_vNN.ext

- Before generating, inspect both the target directory and its Archive/
  directory to find the next version.
- Write the next vNN as a new file, then move the superseded file into a nearby
  Archive/ directory without changing its historical filename.
- Never label a file final, old, copy, or latest when an explicit version and
  lifecycle status can express the same fact.

### High-risk filesystem operations [OPTIONAL]

For bulk moves, renames, reorganizations, deduplication, or changes to synced
document libraries:

1. Run a read-only audit and identify protected, restricted, dirty, placeholder,
   or unavailable files.
2. Produce an explicit source-to-destination manifest, one mapping per line.
3. Record source hashes, exact timestamps when relevant, link/reference impact,
   and collision checks.
4. Present the exact plan and validation result for human review. Bind approval
   to an immutable plan identifier or digest when the risk justifies it.
5. Apply only the approved mappings through one designated writer.
6. Write atomically, refuse occupied destinations, and never treat a collision
   as permission to overwrite or auto-rename.
7. Independently verify destination presence, expected source absence, hashes,
   links, byte preservation, exact timestamps, and manifest status.
8. Stop on any mismatch, unknown sync state, partial rollback, or stale approval.
   Do not begin the next batch.

- Prefer archive or trash over deletion. When Git is unavailable, retain the
  manifest and checksums as the recovery record.
- For content-addressed deduplication, require a cryptographic hash match,
  update every reference, verify no references remain, then remove only the
  proven duplicate.

## 9. Implementation and validation

### Change design

- Maintain clear component and process boundaries. Do not bypass the documented
  coordinator, service, interface, or protocol path.
- Keep provider integrations in adapters. Core roles and contracts should
  describe semantic actions instead of pinning one vendor, tool-call schema, or
  dated model ID.
- When changing a shared field or interface, update all producers, consumers,
  schemas, examples, tests, and documentation together.
- Prefer verifiable requirements and acceptance criteria. Replace vague words
  such as fast, robust, easy, or secure with a measurable condition or a tagged
  assumption.
- Verification confirms the implementation meets a requirement. Validation
  confirms the result meets the user's real need. Do not substitute one for the
  other.

### Checks

- Discover the repository's actual commands from package files, presets,
  workflows, and nearby documentation; do not invent a standard command.
- Run the smallest safe check that exercises the change, then the broader
  relevant suite in proportion to risk.
- Typical gates: format, lint, typecheck, unit tests, integration/contract tests,
  build, security/privacy checks, schema validation, and branch/path guards.
- Use synthetic fixtures for public or privacy-sensitive repositories. Do not
  validate with real customer or personal records.
- If an external service is unavailable, verify local behavior and state the
  unverified integration plainly.
- Render and visually inspect documents, PDFs, slides, spreadsheets, images,
  and responsive UI when layout matters. A successful build or page count is
  not visual validation.
- Re-run relevant checks after every fix that can invalidate an earlier result.

### Proportional re-review

When an existing artifact changes:

- Changed documents receive a full review from their responsible owner.
- Unchanged documents receive only a cross-reference scan for stale names,
  IDs, values, sections, constraints, and dependencies.
- Do not re-derive or re-summarize unchanged content without cause.
- A previously certified or approved artifact returns to unapproved status when
  a material source changes; re-run the relevant gate.

## 10. Multi-agent operation [OPTIONAL]

Use multiple agents only when roles have independent, bounded work and the
coordination cost is justified.

When starting from the Agent-Template repository, reusable role guides live in
.agents/templates/. Copy only the roles the project needs, give them
project-specific names and exact paths, and delete every unused placeholder.
The root AGENTS.md remains authoritative.

### Role definition

Every role guide should specify:

- Persona and purpose.
- Objective and definition of done.
- Required inputs and prerequisite files.
- Exact output paths and formats.
- Responsibilities and checkpoint unit.
- Files it may write and files it must not write.
- Collaboration handoffs and structured return format.
- Escalation triggers and decisions reserved for humans.
- Quality gates, prohibited actions, and suitable model/resource tier.

Prefer current capability tiers over dated model IDs:

- Check the models and capabilities currently available before selecting or
  hardcoding a route.
- Fast: mechanical audits, extraction, status summaries, and classification.
- Balanced: research, coordination, planning, writing, and routine coding.
- Powerful: high-stakes architecture, safety, security, adversarial exit gates,
  or a demonstrably failed Balanced attempt.

### Ownership and serialization

- Give each artifact one owner. A specialist writes only its named artifact and
  returns all cross-file effects as proposals.
- Use one coordinator as the sole cross-file integrator, committer, and question
  broker for multi-file workflows. The coordinator checks each handoff; an
  independent Validator/Auditor owns any formal exit-gate verdict.
- Serialize overlapping writes. Independent read-only reviews may run in
  parallel.
- After each worker, validate path ownership, schema, privacy, duplicates,
  context consistency, and checkpoint completeness before dispatching another
  mutation.
- Specialists do not commit unless their role explicitly owns an isolated
  repository or branch.

Customize the ownership table:

| Role | May read | May write | Must not write | Checkpoint unit |
| --- | --- | --- | --- | --- |
| coordinator | Task-scoped context | Validated cross-file updates and commits | Specialist-owned content | One validated handoff |
| researcher | Assigned sources and context | One research topic | Product state, decisions, Git | One completed question |
| implementer | Assigned code surface | Owned implementation and tests | Unrelated modules | One coherent change |
| reviewer | Relevant diff and sources | Findings only, or nothing | Product files and commits | One finding |
| privacy gate | Plan/diff plus provenance | Approval list or verdict | Another role's prose | One claim |

### Independence and handoffs

- Use blind or independent reviewers when shared context would create anchoring
  or groupthink. Have the coordinator deduplicate after their reports exist.
- A reviewer attacks the artifact, not its author, and anchors every finding to
  a path, line, section, requirement, or stable ID.
- Every finding includes severity, evidence, impact, and a proposed resolution.
- Cap handoffs to the most material machine-consumable lines when the
  coordinator must merge many reports; keep full evidence in the durable file.
- Use structured, human-readable Markdown status blocks and tables across
  stages. Preserve unknown values rather than coercing them into a conclusion.
- Verify prerequisite output files exist before routing the next role. A claimed
  completion without its durable artifact does not pass the gate.

### Readiness and convergence gates

- Define readiness modes such as research, draft, review-ready, filing-ready, or
  production-ready with explicit evidence requirements.
- If a gate is missing, downgrade the effective mode and list every gap. Never
  preserve a requested label that the evidence does not support.
- For iterative work, maintain an ambiguity or risk register with stable IDs,
  explicit states, owners, severity, decisions, assumptions, and rationale.
- Route ambiguity as ASSUME when cheap to reverse, RESEARCH when evidence can
  answer it, or ASK when only the user can decide and the blast radius matters.
- Every question includes a recommended default and consequence if wrong.
- Define binary exit criteria where possible. If the criteria do not all pass,
  the result is not certified.

## 11. Documentation and continuous improvement

- Keep decisions, assumptions, risks, and open questions in durable files rather
  than relying on chat history.
- Store facts once and compute derived aggregates. A stored count or duplicate
  title drifts and eventually lies.
- Use closed vocabularies for fields agents normalize. Proposed values enter a
  decision queue and become valid only after approval.
- Prefer one key, one meaning, and one type across the repository.
- Keep generated prose structurally distinguishable from human-authored source
  when authorship matters.
- Maintain a retrospective log. After a failure or user correction, fold the
  durable lesson into the canonical contract or role guide and record the
  reason. Let failures improve the rules.
- Do not copy private source bodies into process documentation. Record durable
  process decisions and high-level outcomes only.

### Review against the canonical template [OPTIONAL]

When asked to bring forward general practices from `mcleu/Agent-Template`, use
the current `main` version of its `ADOPTION.md` as the comparison procedure.

- Start audit-only and identify both the template commit and local commit.
- Compare practices rather than synchronizing files or headings.
- Write the adoption matrix incrementally to a locally governed durable path.
- Preserve stricter local and project-specific rules; escalate material
  conflicts instead of silently choosing one.
- Propose exact target files and wording before implementation unless the user
  already authorized the change.
- Update canonical `AGENTS.md` before `CLAUDE.md` or another runtime adapter, and
  validate that shared policy is not duplicated or contradictory.
- Never copy unresolved placeholders, example paths, commands, branch names, or
  optional modules into the project.

## 12. Completion and handoff

Before declaring work complete:

- [ ] Requested outcome exists at the agreed path.
- [ ] Every changed file was re-read after the final edit.
- [ ] Scope and ownership boundaries were respected.
- [ ] No private, generated, vendor, or unrelated file was accidentally added.
- [ ] Relevant format, lint, type, test, build, schema, privacy, branch, and
      visual checks passed, or each unrun check is named with the reason.
- [ ] The final diff and staged diff were reviewed.
- [ ] Tracked work is committed on the correct feature branch.
- [ ] The branch was pushed and a pull request opened when a remote/PR path
      exists; the agent did not merge it.
- [ ] CI and review state were checked after the final push.
- [ ] Plans, decision logs, research notes, and checkpoint state reflect what
      actually happened.
- [ ] The handoff states confirmed facts, remaining tasks, deadlines, risks, and
      explicit unknowns.

Lead the final report with the outcome. Include:

1. Files created or changed.
2. Commit and branch.
3. Pull request and CI state, or the explicit no-remote/no-CI limitation.
4. Checks run and their results.
5. Open risks, approval gates, and next action.

Do not claim that everything is in place when bookings, credentials, external
integrations, approvals, deadlines, or evidence remain unknown.

## 13. Project-specific contract [CUSTOMIZE BEFORE USE]

### Authoritative trunk and branch policy

- Trunk:
- Allowed branch prefixes:
- Worktree requirements:
- Commit format:
- Pull-request policy:

### Commands

- Install:
- Develop:
- Format:
- Lint:
- Typecheck:
- Unit tests:
- Integration tests:
- Build:
- Privacy/public-safety check:
- Visual or artifact validation:

### Real folder map

| Path | Purpose | Owner | Privacy/retention |
| --- | --- | --- | --- |
| [CUSTOMIZE] | | | |

### Sources of truth and schemas

| Subject | Authority | Consumers that must remain aligned |
| --- | --- | --- |
| [CUSTOMIZE] | | |

### Restricted paths and prohibited actions

- [CUSTOMIZE]

### Readiness gates

| Mode | Required evidence | Permitted output |
| --- | --- | --- |
| research | | |
| draft | | |
| review-ready | | |
| production-ready | | |

### Approval gates

- [CUSTOMIZE: external actions]
- [CUSTOMIZE: destructive operations]
- [CUSTOMIZE: publication or privacy]
- [CUSTOMIZE: regulated, legal, financial, or production decisions]

### Definition of done

- [CUSTOMIZE: project-specific binary completion criteria]
