---
schema_version: 1
type: versioning_policy
template_id: versioning-policy
document_version: "1.0"
last_edited: "2026-08-05"
---

# Versioning Policy Template

> Copy this file to `VERSIONING.md`, replace every `[CUSTOMIZE]` field, and
> remove version surfaces the project does not use. `AGENTS.md` remains the
> working contract; this file defines how project artifacts identify change.

## 1. Version surfaces

Do not use one number to mean several kinds of change.

| Surface | Identifier and location | Authority | Bump owner | Compatibility promise |
| --- | --- | --- | --- | --- |
| Product or package release | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |
| Data or interface schema | Integer `schema_version` + `schemas/vN/` | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |
| Durable document content | Two-part `document_version` + document-control block | Each governed document | Document owner | Prior history rows preserved |
| Human-facing deliverable | [CUSTOMIZE: for example, filename `vNN`] | [CUSTOMIZE] | [CUSTOMIZE] | Prior versions preserved |
| Migration or manifest | [CUSTOMIZE: stable ID or digest] | [CUSTOMIZE] | [CUSTOMIZE] | Immutable once approved/applied |
| Source revision | Git commit SHA and release tag | Git | Authorized integrator | Immutable revision identity |

- A Git branch, commit, or tag identifies source state. It does not replace a
  schema version, document version, deliverable filename version, migration ID,
  or product release.
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

Use positive integer schema versions by default. Version `N` lives under
`schemas/vN/`, and every governed structured artifact declares
`schema_version: N` plus a stable `type`.

- **Clarification**: accepted/emitted structure and behavior do not change. Keep
  the current schema version.
- **Additive-compatible**: adds an optional field or value. Keep the current
  version only when that schema explicitly permits unknown future fields and
  every existing consumer preserves or safely ignores the extension.
- **Breaking**: removes/renames a required field, changes a field's type or
  meaning, narrows accepted values, changes identity/lifecycle rules, or
  requires consumer migration. Create the next integer version directory.

Never edit a released `schemas/vN/` definition into a different contract,
reuse/decrement a schema version, or treat a product SemVer bump as a schema
version. The project's actual compatibility window is: [CUSTOMIZE].

### Human-facing deliverables [OPTIONAL]

- Filename pattern: [CUSTOMIZE: for example,
  `YYYY-MM-DD_Project_Subject_Deliverable_vNN.ext`].
- Working-state naming: [CUSTOMIZE].
- Archive path: [CUSTOMIZE].
- Version authority: inspect both the active and archive locations before
  choosing the next number.

### Durable human-authored documents

Every durable operating guide, role guide, plan, research file, decision log,
review, audit, report, or similar authored document follows
[schemas/v1/document-control.md](schemas/v1/document-control.md) or a stricter
local equivalent.

- Use two-part `MAJOR.MINOR` document versions. Working drafts use `0.x`; the
  first reviewed baseline is `1.0`.
- Increment `MINOR` for a material correction, addition, or refinement that
  preserves the document's purpose and governing structure. Increment `MAJOR`
  when purpose, required structure, authority, or interpretation changes
  materially while the document keeps the same identity.
- Update the current version, last-edited date, and exactly one specific history
  row once per coherent material revision. Preserve all prior rows.
- Reusable templates declare matching `document_version` and `last_edited`
  metadata. A copied template begins a new document history while retaining its
  schema identity.
- Source code, configuration, generated output, third-party inputs, and
  machine-managed lockfiles use native/Git versions unless a local contract
  explicitly requires an embedded file version.

## 3. Schema change protocol

For every schema or shared-interface change:

1. Identify the canonical schema, current version, owner, producers, consumers,
   fixtures, generated representations, and validators.
2. State the old and proposed contract. Classify the change as clarification,
   additive-compatible, breaking, or a documented project-specific class.
3. Define behavior for missing, unknown, null, invalid, and deprecated values.
   Do not silently coerce an unknown value or reuse a field for a new meaning.
4. Verify the version directory, artifact `schema_version`, stable `type`, and
   introduction baseline. Missing version metadata is not proof of legacy
   status.
5. For a breaking change, create the next integer schema directory and provide
   a migration/backfill plan, rollback or stop condition, support window, and
   consumer cutover order. Preserve the prior version definition.
6. Update the canonical schema, producers, consumers, fixtures, tests,
   documentation, compatibility matrix, and migration tooling in one reviewed
   change—or explicitly gate the safe sequence when atomic release is
   impossible.
7. Run schema validation and consumer contract tests with synthetic fixtures,
   including prior-version and missing/unknown/not-applicable cases.
8. Record the version decision and compatibility result in the pull request.

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
- [ ] Every new or changed structured template/artifact declares the schema
      version and stable type required by its versioned schema directory.
- [ ] Every new or materially changed durable human-authored file has a current
      document version, matching last-edited date/history row, and preserved
      prior history.
- [ ] Compatibility classification and rationale are recorded.
- [ ] Canonical schemas and every producer/consumer remain aligned.
- [ ] Migration, rollback/stop conditions, and deprecation window are defined
      when required.
- [ ] Synthetic fixtures and contract tests cover the old and new behavior.
- [ ] Legacy treatment is supported by an introduction marker, manifest, or
      equivalent baseline rather than inferred from a missing field.
- [ ] Only the authorized version surface was bumped.
- [ ] Git diff, staged diff, branch, commit, PR, and CI state were verified.
- [ ] Publication, deployment, release, and merge gates remain human-controlled.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established schema, document, release, migration, and Git version controls. |
