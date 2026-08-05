# Reusable-template metadata schema v1

Every reusable template has leading structured metadata.

Normal Markdown form:

```yaml
---
schema_version: 1
type: agent_role
template_id: agent-role-example
role: example
document_version: "1.0"
last_edited: "2026-08-05"
---
```

Renderer-owned form, allowed only when YAML frontmatter would become visible or
change the rendered artifact:

```markdown
<!--
schema_version: 1
type: pull_request
template_id: pull-request
document_version: "1.0"
last_edited: "2026-08-05"
-->
```

## Required shared fields

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | integer | Must be `1` for a v1 template and match `schemas/v1/` |
| `type` | string | One of the closed values below |
| `template_id` | string | Stable lower-case identifier matching `[a-z0-9]+(?:-[a-z0-9]+)*` |
| `document_version` | string | Two-part `MAJOR.MINOR` content revision matching the document-control block |
| `last_edited` | date string | ISO `YYYY-MM-DD`, matching the document-control block and current history row |

## Scalar serialization

- Write `schema_version` as an unquoted integer, for example
  `schema_version: 1`. A quoted value such as `"1"` is a string and is invalid.
- Write `document_version` and `last_edited` as quoted strings. Unquoted `1.0`
  may be interpreted as a number, and an unquoted ISO date may be interpreted as
  a date object rather than the required string.
- `type`, `template_id`, and `role` are strings. Values that resemble YAML
  booleans, nulls, numbers, or dates must be quoted when used as strings.
- Validators must check both the value and its scalar type. Coercing a mismatched
  scalar into the expected type is not validation.

Allowed `type` values:

- `agent_contract`
- `versioning_policy`
- `agent_role`
- `schema_contract`
- `pull_request`

An `agent_role` also requires `role`, using the same stable lower-case identifier
format. The role skeleton uses `role: custom`; the downstream project replaces
it with the real role slug when adopting the template.

## Identity and validation

- `template_id` identifies the reusable shape. Do not rename or reuse it for a
  different template meaning within v1.
- Instantiated artifacts retain `schema_version`, `type`, and `template_id` so a
  validator can select the correct rules without guessing from a filename.
- Every reusable template also follows [document-control.md](document-control.md).
  `document_version` tracks this file's content revision, not its schema or Git
  revision. When a copied template becomes a new document, reset its document
  version to the governed draft/baseline value and begin its own history.
- Blank canonical templates may contain `[CUSTOMIZE]` in body/configuration
  fields. Instantiated files must resolve every placeholder required by their
  governing contract.
- Unknown future metadata fields are permitted, but v1 consumers must preserve
  or safely ignore them. They cannot override a required v1 field.
- Missing version metadata on a new or changed template is an error. A warning
  for an unversioned legacy artifact is allowed only with a reviewable
  introduction baseline.

Changing a required field, allowed type, field meaning, or identifier syntax is
a breaking metadata change and requires a new version directory.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.1

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Added distinct schema and per-file document metadata for reusable templates. |
| 1.1 | 2026-08-05 | Required type-preserving scalar serialization and validation without coercion. |
