# Scripts Overview

This folder contains utility scripts used to build, convert, and upload FAIR Package Registry data.

## Python dependencies

Most scripts rely on external Python packages.

Install all required packages with:

```bash
python3 -m pip install requests pyyaml rdflib openpyxl pydantic
```

## Files in this folder

### `package_statements.py`

Generates an RDF Turtle file (`.ttl`) from a FAIR package statement YAML file.

The script validates the YAML first against a versioned input contract before creating RDF.
If the input violates the contract, conversion stops with a validation error.

- Input: one YAML file, for example `src/data/aft_ps.yaml`
- Output: one Turtle file, for example `aft_ps.ttl`
- Used by: `make all-package-statements` in the root `Makefile`

Usage:

```bash
python3 scripts/package_statements.py <input_yaml_file> <output_ttl_file>
```

Example:

```bash
python3 scripts/package_statements.py src/data/aft_ps.yaml aft_ps.ttl
```

Input contract and versioning notes:

- Input YAML must include `schema_version` (semantic version, for example `2.0.0`).
- The contract and migration logic are defined in `scripts/package_statement_contract.py`.
- Supported contract versions:
	- `1.0.0`: backward-compatible mode (legacy-friendly)
	- `2.0.0`: strict mode (enforces stronger cross-reference checks)
- Legacy YAML files without `schema_version` are auto-migrated to `1.0.0`.

Template files:

- Canonical contract-aligned template: `src/data/template_package_statement.yaml`
- Legacy compatibility template: `src/data/template_legacy_1.0.0.yaml`
- Annotated LLM-oriented template: `src/data/templates/template_package_statement_annotated.yaml`

### `xlsx2tsv.py`

Exports a single worksheet from an Excel workbook to one TSV file.

- Input: Excel file path and sheet name
- Output: TSV file for that sheet
- Used by: `make update-tsv-files`

Usage:

```bash
python3 scripts/xlsx2tsv.py <input_xlsx> <sheet_name> <output_tsv>
```

Example:

```bash
python3 scripts/xlsx2tsv.py src/fair-package-registry.xlsx classes src/model/classes.tsv
```

### `tsv2xlsx.py`

Combines multiple TSV files into one Excel workbook, with one sheet per TSV.

- Input: output Excel file path + one or more TSV files
- Output: Excel workbook where each sheet name matches the TSV filename

Usage:

```bash
python3 scripts/tsv2xlsx.py <output_xlsx> <input_tsv_1> [<input_tsv_2> ...]
```

Example:

```bash
python3 scripts/tsv2xlsx.py src/fair-package-registry.xlsx src/model/classes.tsv src/model/object-properties.tsv src/model/data-properties.tsv src/model/instances.tsv src/data/taxonomy.tsv
```

### `fdp_test_data_upload.py`

Uploads dataset metadata records to an FDP instance from the CSV file in `src/data`.

What it does:

- authenticates against an FDP token endpoint
- reads rows from `src/data/ZIN_pakketadviezen_2024_ChatGPT_20250917(2024 Pakketadviezen).csv`
- creates one FDP dataset per row
- publishes each dataset

Important notes:

- This script is configured as a test utility for a specific FDP environment.
- It currently contains hardcoded endpoint and credential values.
- Review and replace these values before running in any other environment.

Usage:

```bash
cd scripts
python3 fdp_test_data_upload.py
```

## Typical workflow

From the repository root:

1. Run `make help` to see available targets.
2. Run `make update-tsv-files` after editing the Excel source.
3. Run `make all` to rebuild ontology, taxonomy, and package statement outputs.
