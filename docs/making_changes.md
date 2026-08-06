# Making changes to the ontology and taxonomy

Edit the terminology sources directly in the Excel sheet or tab-separated files (.tsv) in the [src/](https://github.com/thehyve/fair-package-registry/tree/main/src) folder and rebuild the project. Note that the second line of the source file(s) should contain instructions for ROBOT on how to convert it to OWL.

# Making changes to the example FAIR Package Statements

Edit the YAML files in the [src/](https://github.com/thehyve/fair-package-registry/tree/main/src) folder and rebuild the project.

# Building the project

To rebuild the ontology, taxonomy, and example FAIR Package Statements from source files, use the provided `Makefile`. You will need to have [Make](https://www.gnu.org/software/make/), Python 3, [ROBOT](https://robot.obolibrary.org/), and Java installed on your system.