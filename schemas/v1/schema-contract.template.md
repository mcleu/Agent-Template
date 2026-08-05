---
schema_version: 1
type: schema_contract
template_id: schema-contract
document_version: "1.0"
last_edited: "2026-08-05"
schema_id: "[CUSTOMIZE: stable record or interface identifier]"
status: draft
owner: "[CUSTOMIZE: role or team]"
authority: "[CUSTOMIZE: canonical file or specification]"
compatibility_policy: "[CUSTOMIZE: supported versions and window]"
---

# [CUSTOMIZE: Schema Name] schema v1

## Purpose and boundary

- Represents: [CUSTOMIZE].
- Does not represent: [CUSTOMIZE].
- Source of truth: [CUSTOMIZE].
- File or interface location: [CUSTOMIZE].
- Privacy classification and retention: [CUSTOMIZE].

## Canonical record shape

Show a complete minimal valid record. Every instantiated record carries its
schema version and stable type.

```yaml
---
schema_version: 1
type: [CUSTOMIZE: stable record type]
[CUSTOMIZE: required_field]: [CUSTOMIZE: valid example value]
---
```

## Representations

| Representation | Path or system | Authority or generated | Drift check |
| --- | --- | --- | --- |
| Canonical contract | [CUSTOMIZE] | authority | [CUSTOMIZE] |
| Runtime validator/model | [CUSTOMIZE] | generated/derived | [CUSTOMIZE] |
| Storage representation | [CUSTOMIZE] | derived | [CUSTOMIZE] |
| API or document representation | [CUSTOMIZE] | derived | [CUSTOMIZE] |

## Producers and consumers

| Component or role | Produces/consumes | Supported schema versions | Owner | Contract test |
| --- | --- | --- | --- | --- |
| [CUSTOMIZE] | produces/consumes | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |

## Fields

| Field | Type | Required | Meaning | Allowed values or format | `unknown` / `not_applicable` behavior | Default | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `schema_version` | integer | yes | Selects this record contract | `1` | neither allowed | none | schema |
| `type` | string | yes | Stable record kind | [CUSTOMIZE] | neither allowed | none | schema |
| [CUSTOMIZE] | [CUSTOMIZE] | yes/no | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |

Do not assign a new meaning or type to an existing field. Add a compatible
optional field only when consumers safely preserve or ignore unknown future
fields; otherwise create the next integer schema version with a migration plan.

## Shared conventions

- Required-field presence: [CUSTOMIZE].
- Optional-field absence: [CUSTOMIZE].
- `unknown` means: [CUSTOMIZE].
- `not_applicable` means: [CUSTOMIZE].
- Blank/null behavior: [CUSTOMIZE].
- Unknown future field behavior: [CUSTOMIZE: preserve, ignore safely, or reject].
- Legacy unversioned record policy and evidence baseline: [CUSTOMIZE].

## Invariants

- [CUSTOMIZE: machine-checkable rule].
- [CUSTOMIZE: identity, uniqueness, ordering, range, or relationship rule].
- [CUSTOMIZE: invalid-state behavior].

## Lifecycle or state transitions [OPTIONAL]

| From | Event | To | Preconditions | Rejected behavior |
| --- | --- | --- | --- | --- |
| [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |

## Version and compatibility

- Current schema version: `1`.
- Version directory: `schemas/v1/`.
- Version authority: [CUSTOMIZE].
- Supported producer/consumer versions: [CUSTOMIZE].
- Deprecated fields/values: [CUSTOMIZE or none].
- Deprecation end date or removal condition: [CUSTOMIZE or none].

Classify each change as `clarification`, `additive-compatible`, `breaking`, or a
documented project-specific class. A breaking change creates `schemas/v2/`; do
not rewrite the v1 definition in place.

## Migration and rollback [REQUIRED FOR BREAKING CHANGES]

- Source schema versions: [CUSTOMIZE].
- Target schema version: [CUSTOMIZE].
- Migration/backfill owner and command: [CUSTOMIZE].
- Consumer cutover order: [CUSTOMIZE].
- Rollback or stop condition: [CUSTOMIZE].
- Data preservation and audit evidence: [CUSTOMIZE].
- Support window for prior versions: [CUSTOMIZE].

## Validation and fixtures

- Validator command: [CUSTOMIZE].
- Contract/integration test: [CUSTOMIZE].
- Minimal valid fixture: [CUSTOMIZE].
- Missing/unknown/not-applicable/invalid fixtures: [CUSTOMIZE].
- Prior-version compatibility fixtures: [CUSTOMIZE].
- Generated-representation drift check: [CUSTOMIZE].
- Privacy/public-safety check: [CUSTOMIZE].

## Change record

Keep this concise; link to the reviewed decision or pull request for full
evidence.

| Schema version | Date | Compatibility | Summary | Migration/decision reference |
| --- | --- | --- | --- | --- |
| `1` | [CUSTOMIZE] | initial | [CUSTOMIZE] | [CUSTOMIZE] |

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Document version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the controlled schema-contract template. |
