# Schema Contracts

This directory holds the repository's canonical, versioned data and interface
contracts. Copy [schema.template.md](schema.template.md) for each governed
contract and replace every `[CUSTOMIZE]` field.

Do not place live records, credentials, generated exports, or private examples
here. Fixtures must be synthetic and safe for the repository's audience.

## Registry

Replace this example row with the real schema inventory.

| Schema ID | Current version | Authority | Owner | Producers | Consumers | Validator | Migration path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE: canonical file] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] | [CUSTOMIZE] |

## Rules

- One canonical file owns each schema. Generated models, API documentation,
  examples, database layouts, and runtime validators must identify their source
  and must not become competing authorities.
- Every schema has a stable `schema_id`, explicit `schema_version`, owner,
  status, compatibility policy, producers, consumers, and validation command.
- A field keeps one meaning and type for its lifetime. Rename or version a
  changed concept instead of silently reusing the field.
- Define missing, unknown, null, invalid, and deprecated behavior explicitly.
- Update affected producers, consumers, fixtures, tests, migrations, examples,
  and documentation with the contract change.
- Use synthetic fixtures in a public or privacy-sensitive repository.
- Follow `VERSIONING.md` after installing the root
  [versioning template](../VERSIONING.template.md). Until customized, the
  template is guidance rather than project authority.

## Adding or changing a schema

1. Add the contract to this registry and name its authority and owner.
2. Start from the schema template and inventory every producer and consumer.
3. Classify the compatibility and proposed version change before editing.
4. Define migration, rollback/stop conditions, support window, and cutover order
   for a breaking change.
5. Change the canonical schema and all coupled surfaces in one reviewed change,
   or document the gated release sequence.
6. Validate with synthetic fixtures and contract tests.
7. Record the version rationale, exact checks, and remaining unknowns in the
   pull request; do not merge automatically.
