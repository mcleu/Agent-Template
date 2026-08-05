# Schema Contracts

This scaffold keeps schema definitions in immutable major-version directories.
New repositories start with [v1](v1/README.md). Do not rewrite a released `v1`
contract into a different shape; add `v2/` and a migration path when a breaking
format change is required.

## Version registry

| Schema version | Status | Index | Introduction marker |
| --- | --- | --- | --- |
| `1` | active template baseline | [schemas/v1/README.md](v1/README.md) | [schemas/v1/INTRODUCED.md](v1/INTRODUCED.md) |

## Use

1. Keep the version directory and introduction marker in the commit that adopts
   the schema baseline.
2. Copy [schema-contract.template.md](v1/schema-contract.template.md) within the
   applicable `schemas/vN/` directory for each governed record or interface.
3. Replace every `[CUSTOMIZE]` value and add the schema to that version's index.
4. Put the matching `schema_version: N` and stable `type` in every structured
   template and generated record governed by the schema.
5. Add a validator that rejects unsupported versions, missing required fields,
   invalid closed-vocabulary values, and unresolved template placeholders in
   instantiated artifacts.
6. Decide and document the legacy policy. Missing `schema_version` is not enough
   evidence that a file is legacy; use an introduction marker, migration
   manifest, or another reviewable baseline.
7. Apply [document-control.md](v1/document-control.md) to every durable
   human-authored file. Keep its `document_version` independent of the
   structured artifact's `schema_version`.

## Rules

- Schema versions are positive integers and match their `schemas/vN/`
  directory. Product/package releases may use a different scheme.
- Every reusable template has a required `schema_version`, stable `type`,
  `template_id`, `document_version`, and `last_edited`; agent roles also declare
  `role`.
- A field keeps one meaning and type for the lifetime of a schema version.
- Define required, optional, `unknown`, `not_applicable`, invalid, deprecated,
  and unknown-future-field behavior explicitly.
- Generated models, API documentation, examples, validators, and storage
  layouts identify their canonical schema source. They do not become competing
  authorities.
- Update affected producers, consumers, fixtures, tests, migrations, examples,
  and documentation with a contract change.
- Use synthetic fixtures in public or privacy-sensitive repositories.
- Follow the installed `VERSIONING.md`; the root
  [versioning template](../VERSIONING.template.md) remains guidance until it is
  customized for the downstream project.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the schema scaffold and linked per-file document control. |
