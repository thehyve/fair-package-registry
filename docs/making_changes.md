# Making changes to the ontology and taxonomy

Edit the terminology sources directly in the Excel sheet or tab-separated files (.tsv) in the [src/](https://github.com/thehyve/fair-package-registry/tree/main/src) folder and rebuild the project. Note that the second line of the source file(s) should contain instructions for ROBOT on how to convert it to OWL.

# Making changes to the example FAIR Package Statements

Edit the YAML files in the [src/](https://github.com/thehyve/fair-package-registry/tree/main/src) folder and rebuild the project.

# YAML Contract Versioning

Package Statement YAML input uses a versioned contract with field `schema_version`.

Current versions:

- `1.0.0`: backward-compatible contract for legacy YAML files
- `2.0.0`: strict contract with stronger cross-reference validation

Versioning rules:

- MAJOR: breaking input changes (field rename/removal, changed semantics)
- MINOR: backward-compatible additions (new optional fields)
- PATCH: non-breaking fixes/clarifications

Workflow for contract updates:

1. Update `src/data/template_package_statement.yaml`.
2. Update validation and migration rules in `scripts/package_statement_contract.py`.
3. Update transformation logic in `scripts/package_statements.py` if needed.
4. Bump `schema_version` according to semantic versioning.
5. Rebuild and validate generated Turtle outputs.

Compatibility behavior:

- If `schema_version` is omitted, input is treated as legacy and migrated to `1.0.0`.
- Use `2.0.0` for new/cleaned inputs where strict validation is required.

# Reusing the Contract in Other Repositories

To consume this YAML contract from another pipeline repository:

1. Pin this repository by tag (recommended), for example `v1.0.0`.
2. Read template and contract from that pinned tag, not from `main`.
3. Upgrade only when intentionally adopting a newer contract version.

Recommended files to reference:

- `src/data/template_package_statement.yaml`
- `src/data/template_legacy_1.0.0.yaml` (legacy compatibility template)
- `scripts/package_statement_contract.py`

Annotated companion template files:

- `src/data/templates/template_package_statement_annotated.yaml`
- `src/data/templates/template_annotations_rationale.md`

Pin-by-tag reference pattern for downstream pipelines:

1. Create and push a release tag in this repository (for example `v2.0.0`).
2. In the downstream repository, reference files from that exact tag.

Examples:

- `https://raw.githubusercontent.com/thehyve/fair-package-registry/v2.0.0/src/data/template_package_statement.yaml`
- `https://raw.githubusercontent.com/thehyve/fair-package-registry/v2.0.0/scripts/package_statement_contract.py`
- `https://raw.githubusercontent.com/thehyve/fair-package-registry/v2.0.0/src/data/templates/template_package_statement_annotated.yaml`

Do not reference files from `main` for production pipelines, because contract contents can change between commits.

# Release Playbook (Step-by-Step)

Use this checklist whenever you publish a new template and/or ontology version.

## 1) Decide what changed

Choose one path:

- Template or YAML contract only
- Ontology or taxonomy only
- Both template and ontology/taxonomy

## 2) Decide version bump type

For YAML contract (`schema_version`):

- MAJOR: breaking change (renamed/removed required fields, changed meaning)
- MINOR: backward-compatible additions (new optional fields)
- PATCH: clarifications/fixes without behavior change

For repository tag:

- Use semantic versioning for release tags (for example `v2.1.0`).
- If either template contract or ontology introduces a breaking change, bump MAJOR.

## 3) Update source files

Template/contract updates:

1. Update `src/data/template_package_statement.yaml` (current template).
2. If needed, update `src/data/template_legacy_1.0.0.yaml` only for legacy maintenance.
3. Update `scripts/package_statement_contract.py` (validation + migrations).
4. Update `scripts/package_statements.py` only if mapping logic changes.
5. If annotations changed, update:
	- `src/data/templates/template_package_statement_annotated.yaml`
	- `src/data/templates/template_annotations_rationale.md`

Ontology/taxonomy updates:

1. Update source terms in `src/` (Excel/TSV).
2. Rebuild ontology/taxonomy outputs using Make targets.
3. Confirm generated `fpr-o.ttl` and/or `fpr-tax.ttl` changes are expected.

## 4) Run validation and build checks

1. Run project build targets (`make help` to choose targets).
2. Regenerate example package statements.
3. Ensure legacy examples still pass in compatibility mode.
4. Ensure new template content validates in strict mode (`schema_version: "2.0.0"` until a new strict version is introduced).
5. Review diffs for ontology/template/contract files.

## 5) Update documentation

1. Update this file (`docs/making_changes.md`) if process or version policy changed.
2. Update `scripts/README.md` if file names, dependencies, or workflow changed.
3. Update changelog if used by your team.

## 6) Commit and tag release

1. Commit all related changes together.
2. Push your branch.
3. Create and push a tag (for example `v2.1.0`).

## 7) Roll out to downstream repositories

1. In each downstream pipeline repo, update pinned references from old tag to new tag.
2. Keep stable file paths the same (for example `src/data/template_package_statement.yaml`), only change the tag.
3. Test downstream ingestion with at least one representative YAML.
4. Merge downstream changes only after validation succeeds.

## 8) Deprecation policy (recommended)

1. Keep one legacy contract template (`src/data/template_legacy_1.0.0.yaml`) for migration/testing.
2. Announce deprecation window before removing old migrations.
3. Remove deprecated support only in a MAJOR release.

## Quick decision examples

- Add a new optional YAML field: MINOR bump.
- Rename `intervention-group-id` field: MAJOR bump.
- Fix typo in comments/docs only: PATCH bump.
- Change ontology class meaning in a way that affects mapping: MAJOR bump.

# Building the project

To rebuild the ontology, taxonomy, and example FAIR Package Statements from source files, use the provided `Makefile`. You will need to have [Make](https://www.gnu.org/software/make/), Python 3, [ROBOT](https://robot.obolibrary.org/), and Java installed on your system.

Run `make help` to see the available build targets and a short explanation of what each target does.