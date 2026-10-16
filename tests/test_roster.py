import pytest

from pandavan_economy.roster import REQUIRED_ROSTER_COLUMNS, validate_roster_rows


def row(**overrides):
    result = {column: "" for column in REQUIRED_ROSTER_COLUMNS}
    result.update(
        entity_id="ENT-001",
        entity_name="Example Entity",
        cohort="primary",
        nuclear_set_member="false",
        aaa_set_member="false",
        credit_rating_agency="",
        rating_reference_date="",
        inclusion_rule="",
        evidence_source="",
        evidence_accessed_date="",
        membership_status="proposed",
        notes="Template fixture; not a real roster entry.",
    )
    result.update(overrides)
    return result


def test_proposed_row_can_be_recorded_without_invented_evidence():
    rows = validate_roster_rows([row()])
    assert len(rows) == 1
    assert rows[0]["membership_status"] == "proposed"


def test_verified_aaa_membership_requires_agency_and_reference_date():
    with pytest.raises(ValueError, match="credit_rating_agency"):
        validate_roster_rows([
            row(
                aaa_set_member="true",
                membership_status="verified",
                inclusion_rule="AAA-rated entity",
                evidence_source="https://example.invalid/source",
                evidence_accessed_date="2026-10-16",
            )
        ])


def test_verified_entry_requires_source_and_inclusion_rule():
    with pytest.raises(ValueError, match="inclusion_rule"):
        validate_roster_rows([
            row(
                membership_status="verified",
                evidence_source="https://example.invalid/source",
                evidence_accessed_date="2026-10-16",
            )
        ])


def test_boolean_fields_are_case_normalized():
    result = validate_roster_rows([row(nuclear_set_member="TRUE")])
    assert result[0]["nuclear_set_member"] == "true"


def test_invalid_boolean_is_rejected():
    with pytest.raises(ValueError, match="must be 'true' or 'false'"):
        validate_roster_rows([row(aaa_set_member="yes")])


def test_invalid_cohort_is_rejected():
    with pytest.raises(ValueError, match="cohort"):
        validate_roster_rows([row(cohort="dynamic")])


def test_duplicate_entity_cohort_pair_is_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        validate_roster_rows([row(), row(notes="duplicate")])


def test_same_entity_may_appear_in_both_cohorts():
    result = validate_roster_rows([
        row(cohort="primary"),
        row(cohort="sensitivity"),
    ])
    assert len(result) == 2


def test_frozen_cohort_count_can_be_enforced():
    with pytest.raises(ValueError, match="Expected 15 primary rows"):
        validate_roster_rows([row()], expected_primary_count=15)


def test_verified_aaa_row_with_provenance_passes():
    result = validate_roster_rows([
        row(
            aaa_set_member="true",
            credit_rating_agency="Agency name and rating scale",
            rating_reference_date="2026-10-01",
            inclusion_rule="In AAA-rated set on reference date",
            evidence_source="https://example.invalid/source",
            evidence_accessed_date="2026-10-16",
            membership_status="verified",
        )
    ])
    assert result[0]["membership_status"] == "verified"
