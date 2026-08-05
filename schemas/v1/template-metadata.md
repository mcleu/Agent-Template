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

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Added distinct schema and per-file document metadata for reusable templates. |
