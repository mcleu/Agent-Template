# Agent Template schemas — v1

Every reusable template declares `schema_version: 1`, a stable `type`, and its
own `document_version`/`last_edited` values in structured metadata. Normal
Markdown templates use YAML frontmatter. A renderer-owned template may use an
equivalent leading metadata comment only when frontmatter would leak into or
damage the rendered artifact.

## Shared conventions

- `schema_version` is the integer `1`, not a product release or Git revision.
- `type` is a closed-vocabulary record kind and `template_id` is a stable,
  lower-case hyphenated identity.
- Agent-role templates also require a stable lower-case `role`.
- `document_version` is a two-part content revision governed by
  [document-control.md](document-control.md); it is not the schema version.
- `[CUSTOMIZE]` marks a value that must be resolved when a template is adopted.
  Required metadata fields themselves are never omitted or left blank.
- `unknown` means a field applies but is not known. `not_applicable` means it
  cannot apply. A blank value does not silently mean either state.
- Unknown future metadata fields are permitted for forward compatibility but
  cannot change the meaning or type of a v1 required field.
- Instantiated artifacts retain the template's schema metadata. A validator
  should reject unresolved placeholders in live artifacts while allowing them
  in canonical blank templates.

## Template index

| Type | Required metadata | Template paths | Schema details |
| --- | --- | --- | --- |
| `agent_contract` | shared fields | [AGENTS.template.md](../../AGENTS.template.md) | [template-metadata.md](template-metadata.md) |
| `versioning_policy` | shared fields | [VERSIONING.template.md](../../VERSIONING.template.md) | [template-metadata.md](template-metadata.md) |
| `agent_role` | shared fields + `role` | [agents/templates/](../../agents/templates/) | [template-metadata.md](template-metadata.md) |
| `schema_contract` | shared fields + schema ownership fields | [schema-contract.template.md](schema-contract.template.md) | [schema-contract.template.md](schema-contract.template.md) |
| `pull_request` | shared fields in a leading metadata comment | [PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md) | [template-metadata.md](template-metadata.md) |

Durable authored files that are not reusable templates still follow
[document-control.md](document-control.md), even when they do not need template
identity metadata.

## Compatibility

- Clarifications that do not change accepted or emitted structure remain v1.
- A backward-compatible optional extension may remain v1 only because this
  contract explicitly permits unknown future metadata fields and existing
  consumers preserve or ignore them safely.
- Removing or renaming a required field, changing a field's type or meaning,
  narrowing accepted values, or changing identity/lifecycle rules requires
  `schemas/v2/`, consumer migration, and an explicit support window.
- Schema versions are never reused, decremented, or overwritten in place.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the v1 template schema index and document-control linkage. |
