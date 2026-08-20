import copy
import re
from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

LATEST_SCHEMA_VERSION = "2.0.0"
BACKWARD_COMPAT_SCHEMA_VERSION = "1.0.0"
LEGACY_SCHEMA_VERSION = "0.0.0"
SUPPORTED_SCHEMA_VERSIONS = {BACKWARD_COMPAT_SCHEMA_VERSION, LATEST_SCHEMA_VERSION, LEGACY_SCHEMA_VERSION}

_SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ContractValidationError(ValueError):
    pass


def _clean_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else None
    return str(value)


def _clean_str_list(values: Any) -> list[str]:
    if values is None:
        return []
    if not isinstance(values, list):
        raise TypeError("Expected a list")
    cleaned: list[str] = []
    for value in values:
        text = _clean_str(value)
        if text is not None:
            cleaned.append(text)
    return cleaned


class PackageStatementModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    date: str | date
    package_type: str = Field(alias="package-type")
    package_type_medication_subtype: str | None = Field(default=None, alias="package-type-medication-subtype")
    case_number: int = Field(alias="case-number")
    serial_number: int = Field(alias="serial-number")
    status: str
    contact_person: list[str] = Field(default_factory=list, alias="contact-person")
    see_also: str | None = Field(default=None, alias="see-also")
    guarantee_document: str | None = Field(default=None, alias="guarantee-document")
    iic_assessments: list[str] = Field(default_factory=list, alias="iic-assessments")

    _validate_contact_person = field_validator("contact_person", mode="before")(_clean_str_list)
    _validate_iic_assessments = field_validator("iic_assessments", mode="before")(_clean_str_list)


class PopulationModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    sex: str | None = None
    age: str | None = None
    conditions: list[str] = Field(default_factory=list)
    treatment: list[str] = Field(default_factory=list)

    _validate_conditions = field_validator("conditions", mode="before")(_clean_str_list)
    _validate_treatment = field_validator("treatment", mode="before")(_clean_str_list)


class InterventionModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    applied_intervention: str | None = Field(default=None, alias="applied-intervention")
    intervention_rationale: str = Field(alias="intervention-rationale")
    intervention_classification: str | None = Field(default=None, alias="intervention-classification")
    marketing_authorization_holder: str | None = Field(default=None, alias="marketing-authorization-holder")
    claim_code: int | None = Field(default=None, alias="claim-code")
    care_activity_code: str | None = Field(default=None, alias="care-activity-code")
    care_product_code: str | None = Field(default=None, alias="care-product-code")
    inn: str | None = None
    atc_code: str | None = Field(default=None, alias="atc-code")
    ema_id: str | None = Field(default=None, alias="ema-id")
    costs: float | None = None
    child_interventions: list[str] = Field(default_factory=list, alias="child-interventions")

    _validate_child_interventions = field_validator("child_interventions", mode="before")(_clean_str_list)


class InterventionGroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str | None = None
    intervention_ids: list[str] = Field(default_factory=list, alias="intervention-ids")

    _validate_intervention_ids = field_validator("intervention_ids", mode="before")(_clean_str_list)


class OutcomeModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    name: str
    outcome_classification: str | None = Field(default=None, alias="outcome-classification")
    outcome_measurement: str | None = Field(default=None, alias="outcome-measurement")
    specific_metric: str | None = Field(default=None, alias="specific-metric")
    surrogate_outcome: bool = Field(alias="surrogate-outcome")


class OutcomeGroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    endpoint: str
    outcome_ids: list[str] = Field(default_factory=list, alias="outcome-ids")

    _validate_outcome_ids = field_validator("outcome_ids", mode="before")(_clean_str_list)


class PICOModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    population_ids: list[str] = Field(default_factory=list, alias="population-ids")
    intervention_group_id: str = Field(alias="intervention-group-id")
    comparator_group_id: str = Field(alias="comparator-group-id")
    outcome_group_ids: list[str] = Field(default_factory=list, alias="outcome-group-ids")

    _validate_population_ids = field_validator("population_ids", mode="before")(_clean_str_list)
    _validate_outcome_group_ids = field_validator("outcome_group_ids", mode="before")(_clean_str_list)


class IICAssessmentModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    assessment_type: Literal["Initial", "Reassessment", "Indication extension", "Indication broadening"] | None = Field(default=None, alias="assessment-type")
    intervention_id: str = Field(alias="intervention-id")
    indication_ids: list[str] = Field(default_factory=list, alias="indication-ids")
    emsmp_id: str = Field(alias="emsmp-id")
    bia_id: str = Field(alias="bia-id")
    au_id: str | None = Field(default=None, alias="au-id")
    conclusion: str
    conclusion_text: str = Field(alias="conclusion-text")
    cost_effective: bool = Field(alias="cost-effective")
    managed_entry_agreement_text: str | None = Field(default=None, alias="managed-entry-agreement-text")

    _validate_indication_ids = field_validator("indication_ids", mode="before")(_clean_str_list)


class EMSMPModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    picots_id: str = Field(alias="picots-id")
    slr_id: str = Field(alias="slr-id")
    outcome_measurement_ids: list[str] = Field(default_factory=list, alias="outcome-measurement-ids")
    relative_effectiveness: str | None = Field(default=None, alias="relative-effectiveness")
    adheres_to_emsmps: bool = Field(alias="adheres-to-emsmps")

    _validate_outcome_measurement_ids = field_validator("outcome_measurement_ids", mode="before")(_clean_str_list)


class SystematicLiteratureReviewModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    literature_searches: list[str] = Field(default_factory=list, alias="literature-searches")
    literature_reference_list: str = Field(alias="literature-reference-list")

    _validate_literature_searches = field_validator("literature_searches", mode="before")(_clean_str_list)


class LiteratureSearchModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    label: str
    end_time: str | datetime = Field(alias="end-time")
    target_db: str = Field(alias="target-db")
    target_url: str | None = Field(default=None, alias="target-url")
    evidence_type: Literal["RCT", "Clinical Trial", "Systematic Review"] | None = Field(default=None, alias="evidence-type")
    query: str
    range_beginning: int | None = Field(default=None, alias="range-beginning")
    range_end: int | None = Field(default=None, alias="range-end")


class PublicationModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    type: Literal["JournalArticle", "Manuscript"]
    title: str
    authors: list[str] = Field(default_factory=list)
    journal: str | None = None
    year: int | None = None
    issue: int | None = None
    pages: str | None = None

    _validate_authors = field_validator("authors", mode="before")(_clean_str_list)


class LiteratureReferenceListModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    number_of_items: int = Field(alias="number-of-items")
    references: list[str] = Field(default_factory=list)

    _validate_references = field_validator("references", mode="before")(_clean_str_list)


class StudyModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    registry: str | None = None
    registry_id: str = Field(alias="registry-id")
    url: str | None = None


class CohortModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    study_id: str = Field(alias="study-id")
    intervention_group_id: str = Field(alias="intervention-group-id")


class OutcomeMeasurementModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    type: str | None = None
    cohort_ids: list[str] = Field(default_factory=list, alias="cohort-ids")
    outcome_id: str | None = Field(default=None, alias="outcome-id")
    value: float
    unit: str | None = None
    ci_lower: float | None = Field(default=None, alias="ci-lower")
    ci_upper: float | None = Field(default=None, alias="ci-upper")

    _validate_cohort_ids = field_validator("cohort_ids", mode="before")(_clean_str_list)


class TrendAssumptionModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    scenario_id: str = Field(alias="scenario-id")
    time_points: list[str] = Field(default_factory=list, alias="time-points")
    time_unit: str | None = Field(default=None, alias="time-unit")
    number_of_patients: list[int] = Field(alias="number-of-patients")
    intervention_market_penetration: list[float] | None = Field(default=None, alias="intervention-market-penetration")

    _validate_time_points = field_validator("time_points", mode="before")(_clean_str_list)


class ScenarioModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    description: str


class CostEstimationObservationGroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    type: str
    intervention_ids: list[str] = Field(default_factory=list, alias="intervention-ids")
    number_of_patients: list[int] = Field(alias="number-of-patients")
    total_costs: list[float] = Field(alias="total-costs")

    _validate_intervention_ids = field_validator("intervention_ids", mode="before")(_clean_str_list)


class CostEstimationModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    scenario_id: str = Field(alias="scenario-id")
    trend_assumption_id: str = Field(alias="trend-assumption-id")
    time_points: list[str] = Field(default_factory=list, alias="time-points")
    time_unit: str | None = Field(default=None, alias="time-unit")
    observation_groups: list[CostEstimationObservationGroupModel] = Field(default_factory=list, alias="observation-groups")

    _validate_time_points = field_validator("time_points", mode="before")(_clean_str_list)


class BIAModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    trend_assumption_id: str = Field(alias="trend-assumption-id")
    cost_estimation_ids: list[str] = Field(default_factory=list, alias="cost-estimation-ids")

    _validate_cost_estimation_ids = field_validator("cost_estimation_ids", mode="before")(_clean_str_list)


class AppropriateUseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    title: str
    date: str | None = None
    agreements: list[str] = Field(default_factory=list)

    _validate_agreements = field_validator("agreements", mode="before")(_clean_str_list)


class PackageStatementDocumentModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    schema_version: str = Field(default=LATEST_SCHEMA_VERSION, alias="schema_version")
    package_statement: PackageStatementModel = Field(alias="package-statement")
    populations: list[PopulationModel] = Field(default_factory=list)
    interventions: list[InterventionModel] = Field(default_factory=list)
    intervention_groups: list[InterventionGroupModel] = Field(default_factory=list, alias="intervention-groups")
    outcomes: list[OutcomeModel] = Field(default_factory=list)
    outcome_groups: list[OutcomeGroupModel] = Field(default_factory=list, alias="outcome-groups")
    picots: list[PICOModel] = Field(default_factory=list)
    intervention_indication_combination_assessments: list[IICAssessmentModel] = Field(default_factory=list, alias="intervention-indication-combination-assessments")
    emsmps: list[EMSMPModel] = Field(default_factory=list)
    systematic_literature_reviews: list[SystematicLiteratureReviewModel] = Field(default_factory=list, alias="systematic-literature-reviews")
    literature_searches: list[LiteratureSearchModel] = Field(default_factory=list, alias="literature-searches")
    publications: list[PublicationModel] = Field(default_factory=list)
    literature_reference_lists: list[LiteratureReferenceListModel] = Field(default_factory=list, alias="literature-reference-lists")
    studies: list[StudyModel] = Field(default_factory=list)
    cohorts: list[CohortModel] = Field(default_factory=list)
    outcome_measurements: list[OutcomeMeasurementModel] = Field(default_factory=list, alias="outcome-measurements")
    trend_assumptions: list[TrendAssumptionModel] = Field(default_factory=list, alias="trend-assumptions")
    scenarios: list[ScenarioModel] = Field(default_factory=list)
    cost_estimations: list[CostEstimationModel] = Field(default_factory=list, alias="cost-estimations")
    bias: list[BIAModel] = Field(default_factory=list)
    appropriate_use: AppropriateUseModel | None = Field(default=None, alias="appropriate-use")

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, version: str) -> str:
        cleaned = _clean_str(version)
        if cleaned is None:
            raise ValueError("schema_version cannot be empty")
        if cleaned in SUPPORTED_SCHEMA_VERSIONS:
            return cleaned
        if _SEMVER_PATTERN.match(cleaned):
            raise ValueError(
                f"Unsupported schema_version '{cleaned}'. Supported versions: {sorted(SUPPORTED_SCHEMA_VERSIONS)}"
            )
        raise ValueError(f"Invalid schema_version '{cleaned}'. Must be semantic version, e.g. 1.0.0")

    @model_validator(mode="after")
    def validate_references(self):
        intervention_ids = {item.id for item in self.interventions}
        intervention_group_ids = {item.id for item in self.intervention_groups}
        population_ids = {item.id for item in self.populations}
        outcome_ids = {item.id for item in self.outcomes}
        outcome_group_ids = {item.id for item in self.outcome_groups}
        pico_ids = {item.id for item in self.picots}
        iic_ids = {item.id for item in self.intervention_indication_combination_assessments}
        emsmp_ids = {item.id for item in self.emsmps}
        slr_ids = {item.id for item in self.systematic_literature_reviews}
        literature_search_ids = {item.id for item in self.literature_searches}
        lrl_ids = {item.id for item in self.literature_reference_lists}
        cohort_ids = {item.id for item in self.cohorts}

        errors: list[str] = []

        for group in self.intervention_groups:
            for intervention_id in group.intervention_ids:
                if intervention_id not in intervention_ids:
                    errors.append(f"intervention-groups[{group.id}].intervention-ids references unknown intervention '{intervention_id}'")

        for group in self.outcome_groups:
            for outcome_id in group.outcome_ids:
                if outcome_id not in outcome_ids:
                    errors.append(f"outcome-groups[{group.id}].outcome-ids references unknown outcome '{outcome_id}'")

        for pico in self.picots:
            if pico.intervention_group_id not in intervention_group_ids:
                errors.append(f"picots[{pico.id}].intervention-group-id references unknown intervention group '{pico.intervention_group_id}'")
            if pico.comparator_group_id not in intervention_group_ids:
                errors.append(f"picots[{pico.id}].comparator-group-id references unknown intervention group '{pico.comparator_group_id}'")
            for population_id in pico.population_ids:
                if population_id not in population_ids:
                    errors.append(f"picots[{pico.id}].population-ids references unknown population '{population_id}'")
            for outcome_group_id in pico.outcome_group_ids:
                if outcome_group_id not in outcome_group_ids:
                    errors.append(f"picots[{pico.id}].outcome-group-ids references unknown outcome group '{outcome_group_id}'")

        for iic in self.intervention_indication_combination_assessments:
            if iic.intervention_id not in intervention_ids:
                errors.append(f"intervention-indication-combination-assessments[{iic.id}].intervention-id references unknown intervention '{iic.intervention_id}'")
            for indication_id in iic.indication_ids:
                if indication_id not in population_ids:
                    errors.append(f"intervention-indication-combination-assessments[{iic.id}].indication-ids references unknown population '{indication_id}'")

        for iic_id in self.package_statement.iic_assessments:
            if iic_id not in iic_ids:
                errors.append(f"package-statement.iic-assessments references unknown IIC assessment '{iic_id}'")

        for emsmp in self.emsmps:
            if emsmp.picots_id not in pico_ids:
                errors.append(f"emsmps[{emsmp.id}].picots-id references unknown PICO '{emsmp.picots_id}'")

        for slr in self.systematic_literature_reviews:
            for search_id in slr.literature_searches:
                if search_id not in literature_search_ids:
                    errors.append(f"systematic-literature-reviews[{slr.id}].literature-searches references unknown search '{search_id}'")

        for measurement in self.outcome_measurements:
            for cohort_id in measurement.cohort_ids:
                if cohort_id not in cohort_ids:
                    errors.append(f"outcome-measurements[{measurement.id}].cohort-ids references unknown cohort '{cohort_id}'")

        for cohort in self.cohorts:
            pass

        for trend in self.trend_assumptions:
            if trend.time_points and len(trend.time_points) != len(trend.number_of_patients):
                errors.append(f"trend-assumptions[{trend.id}] time-points length must match number-of-patients length")
            if trend.intervention_market_penetration is not None:
                if trend.time_points and len(trend.time_points) != len(trend.intervention_market_penetration):
                    errors.append(f"trend-assumptions[{trend.id}] time-points length must match intervention-market-penetration length")

        for cost in self.cost_estimations:
            for group in cost.observation_groups:
                for intervention_id in group.intervention_ids:
                    if intervention_id not in intervention_ids:
                        errors.append(
                            f"cost-estimations[{cost.id}].observation-groups[{group.type}].intervention-ids references unknown intervention '{intervention_id}'"
                        )
                if cost.time_points and len(cost.time_points) != len(group.number_of_patients):
                    errors.append(
                        f"cost-estimations[{cost.id}] observation group '{group.type}' number-of-patients length must match time-points length"
                    )
                if cost.time_points and len(cost.time_points) != len(group.total_costs):
                    errors.append(
                        f"cost-estimations[{cost.id}] observation group '{group.type}' total-costs length must match time-points length"
                    )

        for bia in self.bias:
            pass

        if errors:
            raise ValueError("; ".join(errors))

        return self


class StrictPackageStatementDocumentModel(PackageStatementDocumentModel):
    @model_validator(mode="after")
    def validate_strict_references(self):
        intervention_group_ids = {item.id for item in self.intervention_groups}
        emsmp_ids = {item.id for item in self.emsmps}
        slr_ids = {item.id for item in self.systematic_literature_reviews}
        lrl_ids = {item.id for item in self.literature_reference_lists}
        trend_assumption_ids = {item.id for item in self.trend_assumptions}
        scenario_ids = {item.id for item in self.scenarios}
        cost_estimation_ids = {item.id for item in self.cost_estimations}
        bia_ids = {item.id for item in self.bias}

        errors: list[str] = []

        for iic in self.intervention_indication_combination_assessments:
            if iic.emsmp_id not in emsmp_ids:
                errors.append(f"intervention-indication-combination-assessments[{iic.id}].emsmp-id references unknown EMSMP '{iic.emsmp_id}'")
            if iic.bia_id not in bia_ids:
                errors.append(f"intervention-indication-combination-assessments[{iic.id}].bia-id references unknown BIA '{iic.bia_id}'")

        for emsmp in self.emsmps:
            if emsmp.slr_id not in slr_ids:
                errors.append(f"emsmps[{emsmp.id}].slr-id references unknown systematic literature review '{emsmp.slr_id}'")

        for slr in self.systematic_literature_reviews:
            if slr.literature_reference_list not in lrl_ids:
                errors.append(
                    f"systematic-literature-reviews[{slr.id}].literature-reference-list references unknown list '{slr.literature_reference_list}'"
                )

        for cohort in self.cohorts:
            if cohort.intervention_group_id not in intervention_group_ids:
                errors.append(f"cohorts[{cohort.id}].intervention-group-id references unknown intervention group '{cohort.intervention_group_id}'")

        for trend in self.trend_assumptions:
            if trend.scenario_id not in scenario_ids:
                errors.append(f"trend-assumptions[{trend.id}].scenario-id references unknown scenario '{trend.scenario_id}'")

        for cost in self.cost_estimations:
            if cost.scenario_id not in scenario_ids:
                errors.append(f"cost-estimations[{cost.id}].scenario-id references unknown scenario '{cost.scenario_id}'")
            if cost.trend_assumption_id not in trend_assumption_ids:
                errors.append(f"cost-estimations[{cost.id}].trend-assumption-id references unknown trend-assumption '{cost.trend_assumption_id}'")

        for bia in self.bias:
            if bia.trend_assumption_id not in trend_assumption_ids:
                errors.append(f"bias[{bia.id}].trend-assumption-id references unknown trend-assumption '{bia.trend_assumption_id}'")
            for cost_estimation_id in bia.cost_estimation_ids:
                if cost_estimation_id not in cost_estimation_ids:
                    errors.append(f"bias[{bia.id}].cost-estimation-ids references unknown cost-estimation '{cost_estimation_id}'")

        if errors:
            raise ValueError("; ".join(errors))

        return self


def _migrate_legacy_to_1_0_0(data: dict[str, Any]) -> dict[str, Any]:
    migrated = copy.deepcopy(data)
    migrated["schema_version"] = BACKWARD_COMPAT_SCHEMA_VERSION
    return migrated


def migrate_to_latest(data: dict[str, Any]) -> dict[str, Any]:
    version = _clean_str(data.get("schema_version"))
    if version is None:
        return _migrate_legacy_to_1_0_0(data)
    if version in {BACKWARD_COMPAT_SCHEMA_VERSION, LATEST_SCHEMA_VERSION}:
        return copy.deepcopy(data)
    if version == LEGACY_SCHEMA_VERSION:
        return _migrate_legacy_to_1_0_0(data)
    return copy.deepcopy(data)


def validate_and_normalize_document(data: dict[str, Any]) -> dict[str, Any]:
    migrated = migrate_to_latest(data)
    version = _clean_str(migrated.get("schema_version"))
    model_cls: type[PackageStatementDocumentModel]
    if version == LATEST_SCHEMA_VERSION:
        model_cls = StrictPackageStatementDocumentModel
    else:
        model_cls = PackageStatementDocumentModel
    try:
        doc = model_cls.model_validate(migrated)
    except ValidationError as exc:
        raise ContractValidationError(str(exc)) from exc
    except ValueError as exc:
        raise ContractValidationError(str(exc)) from exc
    return doc.model_dump(by_alias=True, exclude_none=True)
