# V1 schema introduction marker

This file marks the commit that introduced schema v1. A downstream validator
may use its first-addition commit to distinguish pre-v1 legacy artifacts from
new or changed artifacts governed by v1.

Do not repurpose, move, or delete this marker. A file without `schema_version`
is legacy only when repository history or an approved migration manifest proves
that it predates this baseline.

## Document control

**Last edited:** 2026-08-05

**Current version:** 1.0

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-05 | Established the immutable v1 schema-introduction marker. |
