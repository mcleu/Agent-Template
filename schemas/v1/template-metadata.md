# Reusable-template metadata schema v1

Every reusable template has leading structured metadata.

Normal Markdown form:

```yaml
---
schema_version: 1
type: agent_role
template_id: agent-role-example
role: example
---
```

Renderer-owned form, allowed only when YAML frontmatter would become visible or
change the rendered artifact:

```markdown
<!--
schema_version: 1
type: pull_request
template_id: pull-request
-->
```

## Required shared fields

| Field | Type | Rule |
| --- | --- | --- |
| `schema_version` | integer | Must be `1` for a v1 template and match `schemas/v1/` |
| `type` | string | One of the closed values below |
| `template_id` | string | Stable lower-case identifier matching `[a-z0-9]+(?:-[a-z0-9]+)*` |

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
