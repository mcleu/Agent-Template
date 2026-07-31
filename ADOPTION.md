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

Produce a durable audit at the path selected by local governance, normally:

    agents/template-adoption.md

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
2. Read the complete local `CLAUDE.md` files and relevant visible `agents/`,
   legacy `.agents/`, `.claude/`, or equivalent role/runtime guidance one or two
   useful layers deep.
3. Inspect the current branch, worktree status, upstream, remotes, and worktrees.
4. Record the local `HEAD` commit and whether the working tree contains unrelated
   changes.
5. Identify the local canonical policy file. Do not assume the repository has
   already made `AGENTS.md` canonical.
6. Do not disturb unrelated edits, switch a dirty worktree, or absorb changes
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

If the local repository still uses `.agents/`, record it as a legacy path and
propose a separate, reference-complete rename to visible `agents/`. Do not create
both active folders or move it during audit-only work.

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
| Checkpointing and resume | Is each natural unit written durably? Can interrupted work resume from the first unfinished unit? |
| Folder and artifact ownership | Are source, work state, research, templates, generated output, private data, and archives separated? Does each artifact have one writer? |
| Evidence and research | Are sources, URLs, check dates, confidence, assumptions, unknowns, and source-of-truth precedence preserved? |
| Privacy and publication | Are private inputs, public output, synthetic examples, secret/PII scans, approval gates, and publication surfaces defined? |
| Planning and ambiguity | Are prerequisite gates, decision owners, approval boundaries, reversibility, and one-question-at-a-time escalation clear? |
| Multi-agent operation | Are roles bounded by exact reads/writes, checkpoints, handoffs, model tiers, and serialized overlapping writes? |
| Review and validation | Are review independence, anchored findings, binary verdicts, actual-artifact checks, visual QA, and stale-check invalidation covered? |
| High-risk filesystem work | Are audit-first plans, exact mappings, collision refusal, provenance, approval binding, sole-writer execution, rollback, and independent verification required where relevant? |
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

Use a matrix like this in `agents/template-adoption.md`:

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
6. Separate straightforward `ADOPT`/`ADAPT` work from `NEEDS_DECISION` items.
7. State the smallest coherent implementation batch.

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
5. Update `CLAUDE.md` last so it points to the canonical policy and retains only
   genuinely Claude-specific runtime instructions.
6. Make the smallest coherent diff. Preserve stricter local rules and verified
   project-specific commands, paths, schemas, role names, and approval gates.
7. Keep the adoption matrix current as each item is implemented, deferred, or
   rejected.
8. Commit logical documentation changes, push the branch, and open a pull
   request when a remote exists. Do not merge the pull request.

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

## 8. Validate the adopted guidance

After the final edit:

- Re-read every changed guidance file in full.
- Confirm instruction hierarchy and path scope remain unambiguous.
- Search for unresolved placeholders, example-only values, obsolete model IDs,
  stale branch names, broken links, nonexistent commands, and invalid paths.
- Check that no local privacy, safety, evidence, approval, or domain rule was
  weakened or dropped.
- Check `AGENTS.md` and `CLAUDE.md` for duplicated or contradictory policy.
- Run documentation lint, link checks, policy tests, branch guards, and privacy
  checks that the local repository provides.
- Run `git diff --check`, inspect the complete diff, stage exact files, and
  inspect the staged diff before committing.
- Record every check with PASS, FAIL, or NOT ASSESSABLE. A skipped required
  check is not a pass.
- Record the final local commit, branch, pull request, and CI state in the audit.

An independent Reviewer or Validator is appropriate when the adoption changes
privacy, destructive-action, publication, regulated, production, or other
high-stakes controls.

## Handoff format

Return a concise, evidence-backed summary:

    TEMPLATE | repo=mcleu/Agent-Template | branch=main | commit=<sha> | checked=<date>
    LOCAL | repo=<path or URL> | branch=<branch> | commit=<sha>
    AUDIT | path=<durable comparison report>
    RESULT | present=<n> | adopt=<n> | adapt=<n> | keep-local=<n> | decision=<n> | not-applicable=<n> | reject=<n>
    CHANGE | <path> | <implemented or proposed practice IDs>
    CHECK | <name> | pass | fail | not-assessable | <evidence>
    OPEN | <decision, risk, approval, unknown, or none>
    NEXT | <smallest safe next action>

Do not say the repository is aligned merely because files were copied or the
diff is empty. Alignment requires practice-level evidence and a clean validation
result.

## Ready-to-use instruction for a future agent

    Compare this repository's authored AGENTS.md, CLAUDE.md, and relevant
    agents/, legacy .agents/, and .claude/ guidance against the current main
    branch of https://github.com/mcleu/Agent-Template using ADOPTION.md from that
    repository. Start audit-only. Read the local rules in full, identify the
    exact template and local commits, and write the practice-by-practice matrix
    incrementally to agents/template-adoption.md (or the locally governed
    equivalent). Preserve stricter and project-specific rules. Do not edit
    guidance until the comparison and proposed first batch are durable and I
    have authorized implementation. If implementation is authorized, use a
    feature branch, make minimal changes to canonical AGENTS.md first and
    CLAUDE.md last, validate the full and staged diffs, commit, push, open a PR,
    and never merge it.
