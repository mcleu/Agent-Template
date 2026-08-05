# Versioning Policy Template

> Copy this file to `VERSIONING.md`, replace every `[CUSTOMIZE]` field, and
> remove version surfaces the project does not use. `AGENTS.md` remains the
> working contract; this file defines how project artifacts identify change.

## 1. Version surfaces

Do not use one number to mean several kinds of change.

| Surface | Identifier and location | Authority | Bump owner | Compatibility promise |
| --- | --- | --- | --- | --- |
| Product or package release | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |
| Data or interface schema | `schema_id` + `schema_version` in `schemas/` | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |
| Human-facing deliverable | [CUSTOMIZE: for example, filename `vNN`] | [CUSTOMIZE] | [CUSTOMIZE] | Prior versions preserved |
| Migration or manifest | [CUSTOMIZE: stable ID or digest] | [CUSTOMIZE] | [CUSTOMIZE] | Immutable once approved/applied |
| Source revision | Git commit SHA and release tag | Git | Authorized integrator | Immutable revision identity |

- A Git branch, commit, or tag identifies source state. It does not replace a
  schema version, document version, migration ID, or product release.
- Do not bump an unrelated surface merely because another surface changed.
- Never use `final`, `latest`, `new`, `old`, or `copy` as a version.

## 2. Version format

### Product or package releases [OPTIONAL]

- Format: [CUSTOMIZE: SemVer, CalVer, or another documented scheme].
- Pre-release format: [CUSTOMIZE].
- Tag format: [CUSTOMIZE: for example, `vMAJOR.MINOR.PATCH`].
- Release notes authority: [CUSTOMIZE].
- Release approval: [CUSTOMIZE].

### Schema and interface contracts

Default to semantic versions unless the repository documents another scheme:

- **MAJOR**: removes or renames a field, changes its type or meaning, narrows an
  accepted value, changes identity/lifecycle semantics, or otherwise requires a
  consumer migration.
- **MINOR**: adds a backward-compatible optional field, value, or capability.
- **PATCH**: clarifies documentation or validation without changing accepted or
  emitted data. A supposed patch that changes observable behavior is not a
  patch.

The project's actual compatibility window is: [CUSTOMIZE].

### Human-facing deliverables [OPTIONAL]

- Filename pattern: [CUSTOMIZE: for example,
  `YYYY-MM-DD_Project_Subject_Deliverable_vNN.ext`].
- Working-state naming: [CUSTOMIZE].
- Archive path: [CUSTOMIZE].
- Version authority: inspect both the active and archive locations before
  choosing the next number.

## 3. Schema change protocol

For every schema or shared-interface change:

1. Identify the canonical schema, current version, owner, producers, consumers,
   fixtures, generated representations, and validators.
2. State the old and proposed contract. Classify the change as major, minor, or
   patch with evidence from the compatibility rules above.
3. Define behavior for missing, unknown, null, invalid, and deprecated values.
   Do not silently coerce an unknown value or reuse a field for a new meaning.
4. For a breaking change, provide a migration/backfill plan, rollback or stop
   condition, support window, and consumer cutover order.
5. Update the canonical schema, producers, consumers, fixtures, tests,
   documentation, compatibility matrix, and migration tooling in one reviewed
   change—or explicitly gate the safe sequence when atomic release is
   impossible.
6. Run schema validation and consumer contract tests with synthetic fixtures.
7. Record the version decision and compatibility result in the pull request.

Generated code or documentation is never the schema authority. Regenerate it
from the canonical contract and verify that no unreviewed drift remains.

## 4. Release and version-bump protocol

- A version bump is a reviewed consequence of an accepted change, not a proxy
  for deciding whether the change is compatible.
- The person or role authorized to bump each surface is named in the table
  above. Other agents propose the bump in their handoff.
- Keep the version change in the same pull request as the behavior it describes,
  unless the repository's release automation requires a separate release PR.
- Do not create a release, publish a package, deploy, or mark a pull request
  ready without the approval required by `AGENTS.md`.
- Verify tags, package metadata, changelogs, deployment configuration, and the
  default branch against actual repository state before making release claims.

## 5. Git traceability

Every versioned change should be traceable through:

    requirement or issue
      -> schema/version decision
      -> feature-branch commits
      -> pull request and checks
      -> approved merge commit
      -> release tag or deployed revision, when applicable

- Use one feature branch per coherent change and one logical concern per commit.
- Never rewrite shared history or move an existing release tag without explicit
  human authorization and a documented recovery plan.
- A draft pull request is the review boundary. Agents may prepare it but do not
  merge or enable auto-merge.
- Record the implementation commit and observed checks in an audit. Report the
  later audit-closure commit and its CI state in the handoff or pull request so
  the audit does not require its own commit recursively.

## 6. Compatibility matrix [CUSTOMIZE]

| Producer version | Consumer version | Supported | Migration or exception | End date |
| --- | --- | --- | --- | --- |
| [CUSTOMIZE] | [CUSTOMIZE] | yes/no | [CUSTOMIZE] | [CUSTOMIZE] |

## 7. Change checklist

- [ ] The affected version surface and its owner are identified.
- [ ] Current versions were read from authoritative files, not recalled.
- [ ] Compatibility classification and rationale are recorded.
- [ ] Canonical schemas and every producer/consumer remain aligned.
- [ ] Migration, rollback/stop conditions, and deprecation window are defined
      when required.
- [ ] Synthetic fixtures and contract tests cover the old and new behavior.
- [ ] Only the authorized version surface was bumped.
- [ ] Git diff, staged diff, branch, commit, PR, and CI state were verified.
- [ ] Publication, deployment, release, and merge gates remain human-controlled.
