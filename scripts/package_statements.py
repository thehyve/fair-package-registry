import types
import urllib.parse
import yaml
import os
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS, PROV, TIME, SDO, DefinedNamespace, ClosedNamespace, DC, DCTERMS, ORG, QB, URIPattern
import sys


class FPR(DefinedNamespace):
    _NS = Namespace("https://w3id.org/zinl/fpr-o#")

    # Classes
    PackageStatement: URIRef
    IICAssessment: URIRef
    EMSMP: URIRef
    LiteratureSearch: URIRef
    SystematicLiteratureReview: URIRef
    LiteratureReferenceList: URIRef
    Scenario: URIRef
    BIA: URIRef
    CostEffectiveness: URIRef
    ManagedEntryAgreement: URIRef
    AppropriateUseAgreement: URIRef
    
    # Classes for value sets (enums)
    PackageType: URIRef
    PackageTypeMedicationSubtype: URIRef
    EditorialStatus: URIRef
    AssessmentType: URIRef
    EvaluationOutcome: URIRef  # Conclusion

    # Object Properties
    hasPackageType: URIRef
    hasPackageTypeMedicationSubtype: URIRef
    hasStatus: URIRef
    hasAssessmentType: URIRef
    hasIndication: URIRef
    hasIntervention: URIRef
    hasIICAssessment: URIRef
    hasEMSMP: URIRef
    hasPICO: URIRef
    hasSystematicLiteratureReview: URIRef
    hasDateLimit: URIRef
    hasEvidenceType: URIRef
    hasOutcomeMeasurement: URIRef
    hasBIA: URIRef
    hasScenario: URIRef
    hasTrendAssumption: URIRef
    hasCostEstimation: URIRef
    hasConclusion: URIRef  # Positive/Negative
    hasRelativeEffectiveness: URIRef  # Positive/Equal/Negative
    hasCostEffectiveness: URIRef
    hasManagedEntryAgreement: URIRef
    
    # Data Properties
    hasCaseNumber: URIRef
    hasSerialNumber: URIRef
    hasGuaranteeDocument: URIRef
    hasMarketingAuthorizationHolder: URIRef
    hasClaimCode: URIRef
    hasCareActivityCode: URIRef    # ZA-code
    hasCareProductCode: URIRef   # Zorgproduct code
    hasINN: URIRef
    hasATCCode: URIRef
    hasEMARef: URIRef
    hasNumberOfPatients: URIRef
    hasTotalCosts: URIRef
    hasMarketPenetration: URIRef
    hasTimepoint: URIRef
    hasCostType: URIRef
    hasConclusionText: URIRef
    adheresToEMSMP: URIRef  # True/False
    isCostEffective: URIRef  # True/False
    isSurrogateOutcome: URIRef  # True/False

    # Instances
    PointOfView: URIRef
    Advice: URIRef
    LockProcedureDrug: URIRef  # Medication subtype
    Definitive: URIRef  # Status
    InitialAssessment: URIRef
    Reassessment: URIRef
    IndicationExtension: URIRef
    IndicationBroadening: URIRef
    Positive: URIRef
    Negative: URIRef
    Equal: URIRef
    Current: URIRef
    Substitution: URIRef
    Additional: URIRef
    Total: URIRef

class OBI(DefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/OBI_")

    ClinicalTrial = URIRef("http://purl.obolibrary.org/obo/OBI_0003699")


class PICO(DefinedNamespace):
    _NS = Namespace("http://data.cochrane.org/ontologies/pico/")

    # Classes
    PICO: URIRef
    Population: URIRef
    Intervention: URIRef
    Outcome: URIRef
    PopulationGroup: URIRef
    InterventionGroup: URIRef
    OutcomeGroup: URIRef

    # Properties
    sex: URIRef
    age: URIRef
    condition: URIRef
    treatment: URIRef
    appliedIntervention: URIRef
    interventionRationale: URIRef
    interventionClassification: URIRef
    childIntervention: URIRef
    intervention: URIRef
    outcome: URIRef
    population: URIRef
    interventionGroup: URIRef
    comparatorGroup: URIRef
    outcomeGroup: URIRef
    outcomeClassification: URIRef
    outcomeMeasurement: URIRef
    endpoint: URIRef
    specificMetric: URIRef
    
class FABIO(DefinedNamespace):
    _NS = Namespace("http://purl.org/spar/fabio/")
    
    SystematicLiteratureReview: URIRef
    JournalArticle: URIRef
    Manuscript: URIRef

class IAO(DefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/IAO_")
    
    isAbout = URIRef("http://purl.obolibrary.org/obo/IAO_0000136")
    isQualityMeasurementOf = URIRef("http://purl.obolibrary.org/obo/IAO_0000221")
    hasMeasurementUnitLabel = URIRef("http://purl.obolibrary.org/obo/IAO_0000039")

class STATO(DefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/STATO_")
    
    # Classes
    Cohort = URIRef("http://purl.obolibrary.org/obo/STATO_0000203")
    StandardizedMeanDifference = URIRef("http://purl.obolibrary.org/obo/STATO_0000176")
    MeanDifference = URIRef("http://purl.obolibrary.org/obo/STATO_0000457")
    MedianDifference = URIRef("http://purl.obolibrary.org/obo/STATO_0000617")
    AbsoluteDifference = URIRef("http://purl.obolibrary.org/obo/STATO_0000614")
    HazardRatio = URIRef("http://purl.obolibrary.org/obo/STATO_0000677")
    RelativeRisk = URIRef("http://purl.obolibrary.org/obo/STATO_0000245")
    CI95 = URIRef("http://purl.obolibrary.org/obo/STATO_0000196")
    
    # Properties
    hasValue = URIRef("http://purl.obolibrary.org/obo/STATO_0000129")
    lowerLimit = URIRef("http://purl.obolibrary.org/obo/STATO_0000315")
    upperLimit = URIRef("http://purl.obolibrary.org/obo/STATO_0000314")

class RO(DefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/RO_")
    
    # Properties
    participatesIn = URIRef("http://purl.obolibrary.org/obo/RO_0000056")
    concretizes = URIRef("http://purl.obolibrary.org/obo/RO_0000059")
    hasPart = URIRef("http://purl.obolibrary.org/obo/BFO_0000051")

class UO(DefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/UO_")
    
    percent = URIRef("http://purl.obolibrary.org/obo/UO_0000187")
    milliliter = URIRef("http://purl.obolibrary.org/obo/UO_0000098")
    month = URIRef("http://purl.obolibrary.org/obo/UO_0000035")



TAX = Namespace("https://w3id.org/zinl/fpr-tax#")


def addLitIfPresent(g: Graph, subject: URIRef, predicate: URIRef, col, key: str) -> Graph:
    obj = col.get(key)
    if obj is None:
        return g
    g.add((subject, predicate, Literal(obj)))
    return g

def addIntIfPresent(g: Graph, subject: URIRef, predicate: URIRef, col, key: str) -> Graph:
    obj = col.get(key)
    if obj is None:
        return g
    g.add((subject, predicate, Literal(obj, datatype=XSD.integer)))
    return g

# TODO: Use different local name pattern
def getTaxonomyTerm(label: str) -> URIRef:
    encoded_label = urllib.parse.quote(label)
    return TAX[encoded_label]

def addNamespaces(g: Graph):
    g.bind("fpr", FPR)
    g.bind("dcterms", DCTERMS)
    g.bind("dc", DC)
    g.bind("org", ORG)
    g.bind("pico", PICO)
    g.bind("tax", TAX)
    g.bind("fabio", FABIO)
    g.bind("IAO", IAO)
    g.bind("OBI", OBI)
    g.bind("STATO", STATO)
    g.bind("RO", RO)
    g.bind("UO", UO)


def createPackageStatementsFromYaml(inputFileName: str, outputFileName: str):
    # Load YAML data
    with open(inputFileName, 'r') as f:
        data = yaml.safe_load(f)

    # Create RDF graph
    g = Graph()
    addNamespaces(g)

    name = os.path.splitext(os.path.basename(inputFileName))[0]
    NSDATA = Namespace("https://w3id.org/zinl/package-statements/" + name + "#")
    g.bind("data", NSDATA)

    # Add ZIN organisations
    zin = NSDATA["Organization-ZorginstituutNederland"]
    zorg1 = NSDATA["OrganizationalUnit-Department-Zorg-I"]
    teamPackageAndAdvice = NSDATA["OrganizationalUnit-Team-Pakket-en-Advies"]
    g.add((zin, RDF.type, ORG.FormalOrganization))
    g.add((zin, RDFS.label, Literal("Zorginstituut Nederland")))
    g.add((zorg1, RDF.type, ORG.OrganizationalUnit))
    g.add((zorg1, RDFS.label, Literal("Department Zorg I")))
    g.add((zin, ORG.hasUnit, zorg1))
    g.add((teamPackageAndAdvice, RDF.type, ORG.OrganizationalUnit))
    g.add((teamPackageAndAdvice, RDFS.label, Literal("Team Pakket en Advies")))
    g.add((zorg1, ORG.hasUnit, teamPackageAndAdvice))

    # Add package statement
    package = data['package-statement']
    subj = NSDATA[package['id']]
    g.add((subj, RDF.type, FPR.PackageStatement))
    g.add((subj, FPR.hasPackageType, FPR[package['package-type']]))
    medicationSubtype = package.get('package-type-medication-subtype')
    if medicationSubtype:
        g.add((subj, FPR.hasPackageTypeMedicationSubtype, FPR[medicationSubtype]))
    g.add((subj, RDFS.label, Literal(package['title'])))
    g.add((subj, DCTERMS.issued, Literal(package['date'], datatype=XSD.date)))
    g.add((subj, FPR.hasCaseNumber, Literal(package['case-number'], datatype=XSD.integer)))
    g.add((subj, FPR.hasSerialNumber, Literal(package['serial-number'], datatype=XSD.integer)))
    g.add((subj, FPR.hasStatus, FPR[package['status']]))
    for contact in package['contact-person']:
        g.add((subj, DC.contributor, Literal(contact))) # TODO: Use Agent or FOAF
    g.add((subj, DCTERMS.publisher, teamPackageAndAdvice))
    g.add((subj, RDFS.seeAlso, URIRef(package['see-also'])))
    guarantee_document = package.get('guarantee-document')
    if guarantee_document:
        g.add((subj, FPR.hasGuaranteeDocument, URIRef(guarantee_document)))
    for iic in package['iic-assessments']:
        g.add((subj, FPR.hasIICAssessment, NSDATA[iic]))

    # Create populations
    for population in data['populations']:
        subj = NSDATA[population['id']]
        g.add((subj, RDF.type, PICO.Population))
        g.add((subj, RDFS.label, Literal(population['title'])))
        sex = population.get('sex')
        if sex:
            g.add((subj, PICO.sex, getTaxonomyTerm(sex)))
        age = population.get('age')
        if age:
            g.add((subj, PICO.age, getTaxonomyTerm(age)))
        for condition in population['conditions']:
            g.add((subj, PICO.condition, getTaxonomyTerm(condition)))
        for treatment in population.get('treatment', []):
            g.add((subj, PICO.treatment, getTaxonomyTerm(treatment)))

    # Create interventions
    for intervention in data['interventions']:
        subj = NSDATA[intervention['id']]
        g.add((subj, RDF.type, PICO.Intervention))
        g.add((subj, DCTERMS.title, Literal(intervention['title'])))
        g.add((subj, PICO.appliedIntervention, getTaxonomyTerm(intervention['applied-intervention'])))
        g.add((subj, PICO.interventionRationale, Literal(intervention['intervention-rationale'])))
        g.add((subj, PICO.interventionClassification, getTaxonomyTerm(intervention['intervention-classification'])))
        addLitIfPresent(g, subj, FPR.hasMarketingAuthorizationHolder, intervention, 'marketing-authorization-holder')
        addIntIfPresent(g, subj, FPR.hasClaimCode, intervention, 'claim-code')
        addLitIfPresent(g, subj, FPR.hasCareActivityCode, intervention, 'care-activity-code')
        addLitIfPresent(g, subj, FPR.hasCareProductCode, intervention, 'care-product-code')
        # For pharmaceuticals, add drug information:
        addLitIfPresent(g, subj, FPR.hasINN, intervention, 'inn')
        addLitIfPresent(g, subj, FPR.hasATCCode, intervention, 'atc-code')
        addLitIfPresent(g, subj, FPR.hasEMARef, intervention, 'ema-id')
        # TODO: Add schedule, dose, duration
        costs = intervention.get('costs')
        if costs:
            g.add((subj, FPR.hasTotalCosts, Literal(costs, datatype=XSD.float)))
        child_interventions = intervention.get('child-interventions', [])
        for child in child_interventions:
            g.add((subj, PICO.childIntervention, NSDATA[child]))

    # Create intervention groups:
    for interventionGroup in data['intervention-groups']:
        subj = NSDATA[interventionGroup['id']]
        g.add((subj, RDF.type, PICO.InterventionGroup))
        interventionIds = interventionGroup.get('intervention-ids', [])
        for interventionId in interventionIds:
            g.add((subj, PICO.intervention, NSDATA[interventionId]))

    # Create outcomes
    for outcome in data['outcomes']:
        subj = NSDATA[outcome['id']]
        g.add((subj, RDF.type, PICO.Outcome))
        g.add((subj, RDFS.label, Literal(outcome['name'])))
        g.add((subj, PICO.outcomeClassification, getTaxonomyTerm(outcome['outcome-classification'])))
        g.add((subj, PICO.outcomeMeasurement, getTaxonomyTerm(outcome['outcome-measurement'])))
        specificMetric = outcome.get('specific-metric')
        if specificMetric:
            g.add((subj, PICO.specificMetric, getTaxonomyTerm(specificMetric)))
        g.add((subj, FPR.isSurrogateOutcome, Literal(outcome['surrogate-outcome'], datatype=XSD.boolean)))

    # Create outcome groups:
    for outcomeGroup in data['outcome-groups']:
        subj = NSDATA[outcomeGroup['id']]
        g.add((subj, RDF.type, PICO.OutcomeGroup))
        g.add((subj, PICO.endpoint, Literal(outcomeGroup['endpoint'])))
        outcomeIds = outcomeGroup.get('outcome-ids', [])
        for outcomeId in outcomeIds:
            g.add((subj, PICO.outcome, NSDATA[outcomeId]))

    # Create PICO
    for picots in data['picots']:
        subj = NSDATA[picots['id']]
        g.add((subj, RDF.type, PICO.PICO))
        for populationId in picots.get('population-ids', []):
            g.add((subj, PICO.population, NSDATA[populationId]))
        g.add((subj, PICO.interventionGroup, NSDATA[picots['intervention-group-id']]))
        g.add((subj, PICO.comparatorGroup, NSDATA[picots['comparator-group-id']]))
        for outcomeId in picots.get('outcome-group-ids', []):
            g.add((subj, PICO.outcome, NSDATA[outcomeId]))

    # Create intervention-hasIndication-combination-assessments
    for iic in data['intervention-indication-combination-assessments']:
        subj = NSDATA[iic['id']]
        g.add((subj, RDF.type, FPR.IICAssessment))
        assessmentType = iic.get('assessment-type')
        if assessmentType == "Initial":
            g.add((subj, FPR.hasAssessmentType, FPR.InitialAssessment))
        elif assessmentType == "Reassessment":
            g.add((subj, FPR.hasAssessmentType, FPR.Reassessment))
        elif assessmentType == "Indication extension":
            g.add((subj, FPR.hasAssessmentType, FPR.IndicationExtension))
        elif assessmentType == "Indication broadening":
            g.add((subj, FPR.hasAssessmentType, FPR.IndicationBroadening))
        g.add((subj, FPR.hasIntervention, NSDATA[iic['intervention-id']]))
        for indicationId in iic.get('indication-ids', []):
            g.add((subj, FPR.hasIndication, NSDATA[indicationId]))
        g.add((subj, FPR.hasEMSMP, NSDATA[iic['emsmp-id']]))
        g.add((subj, FPR.hasBIA, NSDATA[iic['bia-id']]))
        g.add((subj, FPR.hasConclusion, FPR[iic['conclusion']]))
        g.add((subj, FPR.hasConclusionText, Literal(iic['conclusion-text'])))
        ## Add Costeffectiveness
        costEffectiveness = BNode()
        g.add((costEffectiveness, RDF.type, FPR.CostEffectiveness))
        g.add((costEffectiveness, FPR.isCostEffective, Literal(iic['cost-effective'], datatype=XSD.boolean)))
        g.add((subj, FPR.hasCostEffectiveness, costEffectiveness))
        meaText = iic.get('managed-entry-agreement-text')
        if meaText:
            mea = BNode()
            g.add((mea, RDF.type, FPR.ManagedEntryAgreement))
            g.add((mea, SKOS.note, Literal(meaText)))
            g.add((subj, FPR.hasManagedEntryAgreement, mea))

    # Create established medical science and medical practice
    for emsmp in data['emsmps']:
        subj = NSDATA[emsmp['id']]
        g.add((subj, RDF.type, FPR.EMSMP))
        g.add((subj, DCTERMS.title, Literal(emsmp['title'])))
        g.add((subj, FPR.hasPICO, NSDATA[emsmp['picots-id']]))
        g.add((subj, FPR.hasSystematicLiteratureReview, NSDATA[emsmp['slr-id']]))
        # Tie outcome measurements to EMSMP:
        for outcomeMeasurementId in data.get('outcome-measurement-ids', []):
            g.add((subj, FPR.hasOutcomeMeasurement, NSDATA[outcomeMeasurementId]))
        relative_effectiveness = emsmp.get('relative-effectiveness')
        if relative_effectiveness:
            g.add((subj, FPR.hasRelativeEffectiveness, FPR[relative_effectiveness]))
        g.add((subj, FPR.adheresToEMSMP, Literal(emsmp['adheres-to-emsmps'], datatype=XSD.boolean)))

    # Systematic literature reviews
    for slr in data['systematic-literature-reviews']:
        subj = NSDATA[slr['id']]
        g.add((subj, RDF.type, FPR.SystematicLiteratureReview))
        g.add((subj, DCTERMS.title, Literal(slr['title'])))
        for searchId in slr.get('literature-searches', []):
            g.add((subj, DCTERMS.hasPart, NSDATA[searchId]))
        g.add((subj, SDO.result, NSDATA[slr['literature-reference-list']]))
        g.add((NSDATA[slr['literature-reference-list']], PROV.wasGeneratedBy, subj))

    # Literature search
    for search in data['literature-searches']:
        subj = NSDATA[search['id']]
        g.add((subj, RDF.type, FPR.LiteratureSearch))
        g.add((subj, RDFS.label, Literal(search['label'])))
        g.add((subj, PROV.endedAtTime, Literal(search['end-time'], datatype=XSD.dateTime)))
        g.add((subj, SDO.name, Literal(search['target-db'])))
        g.add((subj, SDO.target, URIRef(search['target-url'])))
        g.add((subj, SDO.query, Literal(search['query'])))
        evidenceType = search.get('evidence-type')
        if evidenceType == "Clinical Trial" or evidenceType == "RCT":
            g.add((subj, FPR.hasEvidenceType, OBI.ClinicalTrial))
        elif evidenceType == "Systematic Review":
            g.add((subj, FPR.hasEvidenceType, FABIO.SystematicLiteratureReview))
        elif evidenceType is None:
            pass
        else:
            raise NotImplementedError(f"Evidence type '{evidenceType}' not implemented")
            
        rangeBeginning = search.get('range-beginning')
        rangeEnd = search.get('range-end')
        
        # :YearRange a time:Interval ;
        #   time:hasBeginning [ a time:Instant ; time:inXSDgYear "2000"^^xsd:gYear ] ;
        #   time:hasEnd [ a time:Instant ; time:inXSDgYear "2010"^^xsd:gYear ] .
    
        # Add TIME.hasBeginning and TIME.hasEnd if present
        if rangeBeginning or rangeEnd:
            yearRange = BNode()
            g.add((yearRange, RDF.type, TIME.Interval))
            g.add((subj, FPR.hasDateLimit, yearRange))
            if rangeBeginning:
                beginning = BNode()
                g.add((beginning, RDF.type, TIME.Instant))
                g.add((beginning, TIME.inXSDgYear, Literal(rangeBeginning, datatype=XSD.gYear)))
                g.add((yearRange, TIME.hasBeginning, beginning))
            if rangeEnd:
                end = BNode()
                g.add((end, RDF.type, TIME.Instant))
                g.add((end, TIME.inXSDgYear, Literal(rangeEnd, datatype=XSD.gYear)))
                g.add((yearRange, TIME.hasEnd, end))

    # Publications:
    for publication in data['publications']:
        subj = NSDATA[publication['id']]
        g.add((subj, DCTERMS.title, Literal(publication['title'])))
        publicationType = publication['type']
        if publicationType == "JournalArticle":
            g.add((subj, RDF.type, FABIO.JournalArticle))
        elif publicationType == "Manuscript":
            g.add((subj, RDF.type, FABIO.Manuscript))
        else:
            raise NotImplementedError(f"Publication type '{publicationType}' not implemented")
            # TODO: incomplete mapping
    
    # Literature reference list
    for lrl in data['literature-reference-lists']:
        subj = NSDATA[lrl['id']]
        g.add((subj, RDF.type, FABIO.SystematicLiteratureReview))
        g.add((subj, DCTERMS.title, Literal(lrl['title'])))
        g.add((subj, SDO.numberOfItems, Literal(lrl['number-of-items'], datatype=XSD.integer)))
        for referenceId in lrl.get('references', []):
            g.add((subj, SDO.itemListElement, NSDATA[referenceId]))
            g.add((subj, PROV.hadMember, NSDATA[referenceId]))

    # Studies:
    for study in data['studies']:
        subj = NSDATA[study['id']]
        g.add((subj, RDF.type, OBI.ClinicalTrial))
        g.add((subj, DCTERMS.title, Literal(study['title'])))
        g.add((subj, DCTERMS.source, URIRef(study['registry'])))
        g.add((subj, DCTERMS.identifier, Literal(study['registry-id'])))
        g.add((subj, RDFS.seeAlso, URIRef(study['url'])))
        # TODO: incomplete mapping
        for publicationId in data.get('literature-reference-lists', []):
            g.add((subj, DCTERMS.bibliographicCitation, NSDATA[publicationId]))
            g.add((NSDATA[publicationId], IAO.isAbout, subj))
    
    # Cohorts:
    for cohort in data['cohorts']:
        subj = NSDATA[cohort['id']]
        g.add((subj, RDF.type, STATO.Cohort))
        g.add((subj, RO.participatesIn, NSDATA[cohort['study-id']]))
        g.add((subj, RO.concretizes, NSDATA[cohort['intervention-group-id']]))
    
    # Outcome measurements
    for outcomeMeasurement in data['outcome-measurements']:
        subj = NSDATA[outcomeMeasurement['id']]
        measureType = outcomeMeasurement.get('type')
        if measureType == 'standardized mean difference':
            g.add((subj, RDF.type, STATO.StandardizedMeanDifference))
        elif measureType == 'mean difference':
            g.add((subj, RDF.type, STATO.MeanDifference))
        elif measureType == 'median difference':
            g.add((subj, RDF.type, STATO.MedianDifference))
        elif measureType == 'hazard ratio':
            g.add((subj, RDF.type, STATO.HazardRatio))
        elif measureType == 'risk ratio':
            g.add((subj, RDF.type, STATO.RelativeRisk))
        elif measureType == 'absolute difference':
            g.add((subj, RDF.type, STATO.AbsoluteDifference))
        elif measureType is None:
            pass
        else:
            raise NotImplementedError(f"Outcome measurement type '{measureType}' not implemented")
            # TODO: add other types
        for cohortId in outcomeMeasurement.get('cohort-ids', []):
            g.add((subj, IAO.isAbout, NSDATA[cohortId]))
        g.add((subj, IAO.isQualityMeasurementOf, URIRef(outcomeMeasurement['outcome-id'])))
        g.add((subj, STATO.hasValue, Literal(outcomeMeasurement['value'], datatype=XSD.float)))
        unit = outcomeMeasurement.get('unit')
        if unit == '%':
            g.add((subj, IAO.hasMeasurementUnitLabel, UO.percent))
        elif unit == 'ml':
            g.add((subj, IAO.hasMeasurementUnitLabel, UO.milliliter))
        elif unit == 'months':
            g.add((subj, IAO.hasMeasurementUnitLabel, UO.month))
        elif unit is None:
            pass
        else:
            raise NotImplementedError(f"Outcome measurement unit '{unit}' not implemented")
        # Confidence interval
        ciLower = outcomeMeasurement.get('ci-lower')
        ciUpper = outcomeMeasurement.get('ci-upper')
        
        # Create blank nodes for lower and upper limit, and for CI95
        if ciUpper and ciLower:
            ciLowerBN = BNode()
            g.add((ciLowerBN, RDF.type, STATO.lowerLimit))
            g.add((ciLowerBN, STATO.hasValue, Literal(outcomeMeasurement['ci-lower'], datatype=XSD.float)))
            ciUpperBN = BNode()
            g.add((ciUpperBN, RDF.type, STATO.upperLimit))
            g.add((ciUpperBN, STATO.hasValue, Literal(outcomeMeasurement['ci-upper'], datatype=XSD.float)))
            ci = BNode()
            g.add((ci, RDF.type, STATO.CI95))
            g.add((ci, IAO.isAbout, subj))
            g.add((ci, RO.hasPart, ciLowerBN))
            g.add((ci, RO.hasPart, ciUpperBN))

    # Trend assumptions
    trendAssumptionURIPattern = URIPattern(NSDATA + "DataSet-{id}")
    for trend in data.get('trend-assumptions', []):
        subjDataset = trendAssumptionURIPattern.format(id=trend['id'])
        g.add((subjDataset, RDF.type, QB.DataSet))
        g.add((subjDataset, DCTERMS.title, Literal(trend['title'])))
        g.add((subjDataset, FPR.hasScenario, NSDATA[trend['scenario-id']]))
        for i, timepoint in enumerate(trend.get('time-points', ['default'])):
            postfix = timepoint
            timeUnit = trend.get('time-unit')
            if timeUnit:
                postfix = f"{timeUnit}-{timepoint}"
            subjTimepoint = NSDATA[f"{trend['id']}-{postfix}"]
            g.add((subjTimepoint, RDF.type, QB.Observation))
            g.add((subjTimepoint, QB.dataSet, subjDataset))
            g.add((subjTimepoint, FPR.hasTimepoint, Literal(timepoint)))
            g.add((subjTimepoint, FPR.hasNumberOfPatients, Literal(trend['number-of-patients'][i], datatype=XSD.integer)))
            interventionMarketPenetration = trend.get('intervention-market-penetration')
            if interventionMarketPenetration:
                g.add((subjTimepoint, FPR.hasMarketPenetration, Literal(trend['intervention-market-penetration'][i], datatype=XSD.float)))

    # Scenarios:
    for i, scenario in enumerate(data.get('scenarios', [])):
        subjScenario = NSDATA[scenario['id']]
        g.add((subjScenario, RDF.type, FPR.Scenario))
        g.add((subjScenario, DCTERMS.title, Literal(scenario['title'])))
        g.add((subjScenario, DCTERMS.description, Literal(scenario['description'])))

    # Cost estimations:
    costEstimationPattern = URIPattern(NSDATA + "DataSet-{id}")
    for i, costEstimation in enumerate(data.get('cost-estimations', [])):
        subjCostEstimation = costEstimationPattern.format(id=costEstimation['id'])
        g.add((subjCostEstimation, RDF.type, QB.DataSet))
        g.add((subjCostEstimation, DCTERMS.title, Literal(costEstimation['title'])))
        g.add((subjCostEstimation, FPR.hasScenario, NSDATA[costEstimation['scenario-id']]))
        g.add((subjCostEstimation, PROV.wasDerivedFrom, trendAssumptionURIPattern.format(id=costEstimation['trend-assumption-id'])))
        for observationGroup in costEstimation.get('observation-groups', []):
            costEstimationType = observationGroup['type']            
            for i, timepoint in enumerate(costEstimation.get('time-points', ['default'])):
                postfix = timepoint
                timeUnit = costEstimation.get('time-unit')
                if timeUnit:
                    postfix = f"{timeUnit}-{timepoint}"
                interventionIds = '-'.join(observationGroup.get('intervention-ids', []))
                subjTimepoint = NSDATA[f"{costEstimation['id']}-{interventionIds}-{costEstimationType}-{postfix}"]
                g.add((subjTimepoint, RDF.type, QB.Observation))
                g.add((subjTimepoint, FPR.hasCostType, FPR[costEstimationType]))
                g.add((subjTimepoint, QB.dataSet, subjCostEstimation))
                g.add((subjTimepoint, FPR.hasTimepoint, Literal(timepoint)))
                for interventionId in observationGroup.get('intervention-ids', []):
                    g.add((subjTimepoint, FPR.hasIntervention, NSDATA[interventionId]))
                g.add((subjTimepoint, FPR.hasNumberOfPatients, Literal(observationGroup['number-of-patients'][i], datatype=XSD.integer)))
                g.add((subjTimepoint, FPR.hasTotalCosts, Literal(observationGroup['total-costs'][i], datatype=XSD.float)))

    # BIA:
    for bia in data['bias']:
        subj = NSDATA[bia['id']]
        g.add((subj, RDF.type, FPR.BIA))
        g.add((subj, DCTERMS.title, Literal(bia['title'])))
        trendAssumption = trendAssumptionURIPattern.format(id=bia['trend-assumption-id'])
        g.add((subj, FPR.hasTrendAssumption, trendAssumption))
        for costEstimationId in bia['cost-estimation-ids']:
            costEstimation = costEstimationPattern.format(id=costEstimationId)
            g.add((subj, FPR.hasCostEstimation, costEstimation))

    # Appropriate use agreements
    au = data.get('appropriate-use', [])
    if au:
        subj = NSDATA[au['id']]
        g.add((subj, RDF.type, FPR.AppropriateUseAgreement))
        g.add((subj, DCTERMS.title, Literal(au['title'])))
        date = au.get('date')
        if date:
            g.add((subj, DCTERMS.issued, Literal(date, datatype=XSD.date)))
        for i, agreement in enumerate(au.get('agreements', [])):
            itemUri = NSDATA[f"Agreement-{i}"]
            g.add((subj, DCTERMS.hasPart, itemUri))
            g.add((itemUri, DCTERMS.title, Literal(agreement, lang="nl")))


    # Serialize graph to Turtle to file
    g.serialize(outputFileName, 'turtle', NSDATA)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_yaml_file> <output_ttl_file>")
        sys.exit(1)

    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    createPackageStatementsFromYaml(inputFileName, outputFileName)

