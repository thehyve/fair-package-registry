# FAIR Package Registry PoC

This repository contains sources for the FAIR Package Registry PoC by the Dutch Health Care Institute (Zorginstituut Nederland) and The Hyve.

# Contents

Files:

- [fpr-o.ttl](fpr-o.ttl): OWL ontology for defining FAIR Package Statements
- [fpr-tax.ttl](fpr-tax.ttl): SKOS taxonomy for values such as Conditions.
- [aft_ps.ttl](aft_ps.ttl), [mamma_onco_ps.ttl](mamma_onco_ps.ttl), [trodelvy_ps.ttl](trodelvy_ps.ttl): Three example FAIR Package Statements as machine-readble RDF Turtle files.

Folders:

- [docs/](docs/): HTML/PDF documentation for the FAIR Package Registry ontology and taxonomy.
- [scripts/](scripts/): Scripts for generating the ontology, taxonomy, and example FAIR Package Statements, as well as for uploading example data to a GraphDB instance.
- [src/](src/): Source code for the FAIR Package Registry PoC.
- [use_case/](use_case/): Contains a notebook demonstrating how to query the example FAIR Package Statements, once uploaded to the FAIR data station (GraphDB), using SPARQL.

# Documentation

Documentation as HTML/PDF files can be found in the `docs/` directory. The HTML documentation for the ontology can be generated using [pyLODE](https://github.com/pyLODE/pyLODE), and for the taxonomy using [SKOS Play!](https://skos-play.sparna.fr/play/upload).

# Making changes to the ontology and taxonomy

Edit the terminology sources directly in the Excel sheet or tab-separated files (.tsv) in the [src/](src/) folder and rebuild the project. Note that the second line of the source file(s) should contain instructions for ROBOT on how to convert it to OWL.

# Making changes to the example FAIR Package Statements

Edit the YAML files in the [src/](src/) folder and rebuild the project.

# Building the project

To rebuild the ontology, taxonomy, and example FAIR Package Statements from source files, use the provided `Makefile`. You will need to have [Make](https://www.gnu.org/software/make/), Python 3, [ROBOT](https://robot.obolibrary.org/), and Java installed on your system.

# License

_<todo: add license information here>_

# Contributors

- Eelke van der Horst - The Hyve ([eelkevanderhorst](https://github.com/eelkevanderhorst))
- [Other contributors]


