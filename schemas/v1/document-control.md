# Document-control contract v1

Use this contract for every durable, human-authored document an agent creates or
materially revises: operating guides, role guides, plans, research notes,
decision records, reviews, audits, reports, and human-facing deliverables.

Source code, configuration, generated output, third-party source material, and
machine-managed lockfiles use their native version surface plus Git unless a
project-specific contract explicitly requires embedded file versions. Do not
add noisy version headers to those files merely to satisfy this document rule.

## Adoption and legacy files

- Apply this contract to every new governed document immediately.
- Apply it to an existing governed document when that file is materially
  revised; an adoption-only change does not require a repository-wide retrofit.
- Inventory untouched older documents in a dated introduction baseline or
  migration manifest. Record their observed state and intended treatment
  without inventing versions, dates, approvals, or change history.
- A repository may deliberately schedule a broader retrofit. Keep that work a
  separately reviewed migration with explicit scope and validation.

## Required control block

Place this block near the end of each governed document:

```markdown
## Document control

**Last edited:** YYYY-MM-DD

**Current version:** 0.1

| Version | Date | Change |
| --- | --- | --- |
| 0.1 | YYYY-MM-DD | Initial draft. |
```

A renderer-owned template may put the block in an HTML comment when displaying
it would pollute every rendered instance. The version must still be readable in
the source and machine-checkable.

Reusable structured templates also declare matching leading metadata:

```yaml
document_version: "1.0"
last_edited: "YYYY-MM-DD"
```

The leading values and control block must agree. The control block is the
human-readable file history; Git remains the immutable source-revision history.

## Version progression

Use a two-part `MAJOR.MINOR` document version:

- `0.1`, `0.2`, ... identify working drafts before the first reviewed baseline.
- `1.0` identifies the first reviewed or accepted baseline.
- Increment `MINOR` for a material correction, addition, or refinement that
  preserves the document's purpose and governing structure.
- Increment `MAJOR` when the document keeps its identity but its purpose,
  required structure, authority, or interpretation changes materially.
- Start a new document identity instead of forcing a major bump when the new
  artifact represents a different period, decision, subject, or record.

Do not bump for every keystroke or checkpoint. Reserve the next version when a
coherent change begins, update `Last edited`, and add exactly one concise history
row before handoff. If another material change begins after handoff or review,
advance the version again.

Never decrement or reuse a version. Do not use `final`, `latest`, `new`, `old`,
or `copy` as substitutes for a version or lifecycle status.

## History and corrections

- Keep the newest version row and every prior row; do not rewrite historical
  descriptions to make the present look cleaner.
- A living current-state document may be updated in place with a version bump.
- Preserve dated or approved records. Correct a factual error with a new
  document version and a clearly labeled amendment; do not silently revise the
  historical claim.
- When a workflow uses separately versioned files, inspect active and archive
  locations, create the next unoccupied version, and preserve the superseded
  filename in the governed archive.
- The history summary states what changed, not merely that a file was updated.

## Distinct version surfaces

| Surface | Meaning | Example authority |
| --- | --- | --- |
| `schema_version` | Structure and interpretation of the artifact | `schemas/vN/` |
| `document_version` | Content revision of one durable document | Document control block |
| Product/release version | Shipped product state | Package/release metadata |
| Migration/manifest version | Applied operational change | Approved manifest or migration log |
| Git revision | Exact repository source state | Commit SHA |

An ordinary content edit normally bumps `document_version` without changing
`schema_version`. A structural breaking change may require both, and each bump
must be justified independently.

## Validation

Before handoff, confirm:

- The file has exactly one current version and last-edited date.
- The current version appears in the history table with the same date.
- The version is higher than the prior material revision and was not reused.
- Reusable-template metadata matches the visible or source-readable block.
- The change summary is specific enough to distinguish this revision.
- Schema, document, release, migration, and Git identifiers are not conflated.

## Document control

**Last edited:** 2026-08-08

**Current version:** 1.1

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the v1 document-control contract and two-part file-version rules. |
| 1.1 | 2026-08-08 | Added gradual adoption and truthful baseline handling for untouched legacy documents. |
