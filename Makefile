# Makefile for FAIR Packet statements registry

SRC_DIR=src
TEMP_DIR=tmp

SRC_DATA_DIR=$(SRC_DIR)/data
SRC_MODEL_DIR=$(SRC_DIR)/model
SRC_EXTERNAL_DIR=$(SRC_DIR)/external

# File variables
ROBOT=java -jar robot.jar

PS_XLSX=$(SRC_DIR)/fair-package-registry.xlsx

PS_CLASSES_TSV=$(SRC_MODEL_DIR)/classes.tsv
PS_CLASSES_TTL=$(TEMP_DIR)/classes.ttl
PS_OBJECT_PROPERTIES_TSV=$(SRC_MODEL_DIR)/object-properties.tsv
PS_OBJECT_PROPERTIES_TTL=$(TEMP_DIR)/object-properties.ttl
PS_DATA_PROPERTIES_TSV=$(SRC_MODEL_DIR)/data-properties.tsv
PS_DATA_PROPERTIES_TTL=$(TEMP_DIR)/data-properties.ttl
PS_INSTANCES_TSV=$(SRC_MODEL_DIR)/instances.tsv
PS_INSTANCES_TTL=$(TEMP_DIR)/instances.ttl

TAXONOMY_TSV=$(SRC_DATA_DIR)/taxonomy.tsv
TAXONOMY=fpr-tax.ttl

PREFIXES=$(SRC_DIR)/prefixes.jsonld
GENERIC_ANNOTATION_PROPS=$(SRC_MODEL_DIR)/generic.ttl
ONTOLOGY_ANNOTATIONS=$(SRC_MODEL_DIR)/annotations.ttl
CC_ONTOLOGY=$(SRC_EXTERNAL_DIR)/cochrane-core-ontology.ttl
CPICO_ONTOLOGY=$(SRC_EXTERNAL_DIR)/cochrane-pico-ontology.ttl
PROV_ONTOLOGY=$(SRC_EXTERNAL_DIR)/prov-o.ttl
FABIO_ONTOLOGY=$(SRC_EXTERNAL_DIR)/fabio.ttl
SCHEMAORG_ONTOLOGY=$(SRC_EXTERNAL_DIR)/schemaorg-all-http.ttl
EDAM_ONTOLOGY=$(SRC_EXTERNAL_DIR)/EDAM_1.25.owl
OWL_TIME_ONTOLOGY=$(SRC_EXTERNAL_DIR)/time.ttl
DATA_CUBE_ONTOLOGY=$(SRC_EXTERNAL_DIR)/cube.ttl
STATO_ONTOLOGY=$(SRC_EXTERNAL_DIR)/stato.owl
SKOS_ONTOLOGY=$(SRC_EXTERNAL_DIR)/skos-core.ttl

PS_ONTOLOGY=fpr-o.ttl

PS_AFT_YAML=$(SRC_DATA_DIR)/aft_ps.yaml
PS_AFT_TTL=aft_ps.ttl
PS_MAMMAONCO_YAML=$(SRC_DATA_DIR)/mammaonco_ps.yaml
PS_MAMMAONCO_TTL=mammaonco_ps.ttl
PS_TRODELVY_YAML=$(SRC_DATA_DIR)/trodelvy_ps.yaml
PS_TRODELVY_TTL=trodelvy_ps.ttl


# IRI variables
PS_ONTOLOGY_IRI=https://w3id.org/zinl/fpr-o
TAXONOMY_IRI=https://w3id.org/zinl/fpr-tax
PACKAGE_STATEMENTS_IRI=https://w3id.org/zinl/package-statements


.PHONY: all clean

all: $(PS_ONTOLOGY) $(TAXONOMY) $(all-package-statements)

# # Todo: update
# clean:
# 	rm -f $(PS_ONTOLOGY) $(TAXONOMY)

.PHONY: update-tsv-files

# Update TSV's when Excel changes
$(PS_CLASSES_TSV) $(PS_OBJECT_PROPERTIES_TSV) $(PS_DATA_PROPERTIES_TSV) $(PS_INSTANCES_TSV) $(TAXONOMY_TSV): $(PS_XLSX)
	@echo Updating TSV files
	@for f in $(PS_CLASSES_TSV) $(PS_OBJECT_PROPERTIES_TSV) $(PS_DATA_PROPERTIES_TSV) $(PS_INSTANCES_TSV) $(TAXONOMY_TSV); do \
		echo "Processing $$f"; \
		name="$$(basename "$$f" .tsv)"; \
		python3 scripts/xlsx2tsv.py "$(PS_XLSX)" "$$name" "$$f"; \
	done

# Make tmp/classes.ttl
$(PS_CLASSES_TTL): $(PS_CLASSES_TSV) $(GENERIC_ANNOTATION_PROPS) $(PREFIXES) $(CPICO_ONTOLOGY) $(PROV_ONTOLOGY) \
    $(FABIO_ONTOLOGY) $(SCHEMAORG_ONTOLOGY) $(EDAM_ONTOLOGY) robot.jar
	@echo building package statement ontology classes
	$(ROBOT) \
	merge \
	--input $(CPICO_ONTOLOGY) \
	--input $(GENERIC_ANNOTATION_PROPS) \
	--input $(PROV_ONTOLOGY) \
	--input $(FABIO_ONTOLOGY) \
	--input $(SCHEMAORG_ONTOLOGY) \
	--input $(EDAM_ONTOLOGY) \
	template \
	--add-prefixes $(PREFIXES) \
    --template $(PS_CLASSES_TSV) \
    --ontology-iri "$(PS_ONTOLOGY_IRI)-classes" \
    --output $(PS_CLASSES_TTL)

# Make tmp/object-properties.ttl
$(PS_OBJECT_PROPERTIES_TTL): $(PS_OBJECT_PROPERTIES_TSV) $(GENERIC_ANNOTATION_PROPS) $(PREFIXES) $(CPICO_ONTOLOGY) \
    $(OWL_TIME_ONTOLOGY) $(DATA_CUBE_ONTOLOGY) $(STATO_ONTOLOGY) $(PS_CLASSES_TTL) robot.jar
	@echo building package statement ontology object properties
	$(ROBOT) \
	merge \
	--input $(CPICO_ONTOLOGY) \
	--input $(GENERIC_ANNOTATION_PROPS) \
	--input $(OWL_TIME_ONTOLOGY) \
	--input $(DATA_CUBE_ONTOLOGY) \
	--input $(STATO_ONTOLOGY) \
	--input $(PS_CLASSES_TTL) \
	template \
	--add-prefixes $(PREFIXES) \
    --template $(PS_OBJECT_PROPERTIES_TSV) \
    --ontology-iri "$(PS_ONTOLOGY_IRI)-object-properties" \
    --output $(PS_OBJECT_PROPERTIES_TTL)

# Make tmp/data-properties.ttl
$(PS_DATA_PROPERTIES_TTL): $(PS_DATA_PROPERTIES_TSV) $(GENERIC_ANNOTATION_PROPS) $(PREFIXES) $(CPICO_ONTOLOGY) \
    $(DATA_CUBE_ONTOLOGY) $(PS_CLASSES_TTL) robot.jar
	@echo building package statement ontology data properties
	$(ROBOT) \
	merge \
	--input $(CPICO_ONTOLOGY) \
	--input $(GENERIC_ANNOTATION_PROPS) \
	--input $(DATA_CUBE_ONTOLOGY) \
	--input $(PS_CLASSES_TTL) \
	template \
	--add-prefixes $(PREFIXES) \
    --template $(PS_DATA_PROPERTIES_TSV) \
    --ontology-iri "$(PS_ONTOLOGY_IRI)-data-properties" \
    --output $(PS_DATA_PROPERTIES_TTL)

# Make tmp/instances.ttl
$(PS_INSTANCES_TTL): $(PS_INSTANCES_TSV) $(GENERIC_ANNOTATION_PROPS) $(PREFIXES) $(CPICO_ONTOLOGY) \
    $(DATA_CUBE_ONTOLOGY) $(PS_CLASSES_TTL) robot.jar
	@echo building package statement ontology instances
	$(ROBOT) \
	merge \
	--input $(PS_CLASSES_TTL) \
	template \
	--add-prefixes $(PREFIXES) \
    --template $(PS_INSTANCES_TSV) \
    --ontology-iri "$(PS_ONTOLOGY_IRI)-instances" \
    --output $(PS_INSTANCES_TTL)

# Make fpr-o.ttl
$(PS_ONTOLOGY): $(ONTOLOGY_ANNOTATIONS) $(PS_CLASSES_TTL) $(PS_OBJECT_PROPERTIES_TTL) $(PS_DATA_PROPERTIES_TTL) \
	$(PS_INSTANCES_TTL) robot.jar
	@echo merging package statement ontology components
	$(ROBOT) \
	merge \
	--collapse-import-closure false \
	--add-prefixes $(PREFIXES) \
	--input $(ONTOLOGY_ANNOTATIONS) \
	--input $(PS_CLASSES_TTL) \
	--input $(PS_OBJECT_PROPERTIES_TTL) \
	--input $(PS_DATA_PROPERTIES_TTL) \
	--input $(PS_INSTANCES_TTL) \
	--output $(PS_ONTOLOGY)


# Make taxonomy.ttl
$(TAXONOMY): $(TAXONOMY_TSV) $(GENERIC_ANNOTATION_PROPS) $(CC_ONTOLOGY) $(SKOS_ONTOLOGY) $(PREFIXES) robot.jar
	@echo building taxonomy
	$(ROBOT) \
	merge \
	--input $(CC_ONTOLOGY) \
	--input $(SKOS_ONTOLOGY) \
	--input $(GENERIC_ANNOTATION_PROPS) \
    template \
    --add-prefixes $(PREFIXES) \
    --template $(TAXONOMY_TSV) \
    --ontology-iri "$(TAXONOMY_IRI)" \
    --output $(TAXONOMY)



.PHONY: all-package-statements

# Make Package Statements AFT, MammaOnco, Trodelvy
all-package-statements: $(PS_AFT_YAML) $(PS_MAMMAONCO_YAML) $(PS_TRODELVY_YAML)
	python3 scripts/package_statements.py $(PS_AFT_YAML) $(PS_AFT_TTL)
	python3 scripts/package_statements.py $(PS_MAMMAONCO_YAML) $(PS_MAMMAONCO_TTL)
	python3 scripts/package_statements.py $(PS_TRODELVY_YAML) $(PS_TRODELVY_TTL)


# Make results/model/stato-external-terms-mireot.ttl
# stato-external-terms-mireot.ttl: 
# 	@echo "Creating STATO external terms model"
# 	$(ROBOT) \
# 	extract \
# 	--add-prefixes $(PREFIXES) \
# 	--method mireot \
# 	--input src/model/stato.owl \
# 	--lower-terms $(SRC_MODEL_DIR)/external-terms.txt \
# 	--output $(RESULTS_MODEL_DIR)/stato-external-terms-mireot.ttl




