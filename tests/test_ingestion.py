import pytest

from pandavan_economy.ingestion import OBSERVATION_COLUMNS, validate_observation_rows


def observation(**overrides):
    result = {column: "" for column in OBSERVATION_COLUMNS}
    result.update(
        entity_id="ENT-001",
        entity_name="Example Entity",
        year="2024",
        variable_name="real_interest_rate",
        value="0.025",
        unit="decimal",
        source="Example source",
        source_series_code="RIR",
        frequency="annual",
        reference_period="2024",
        source_release_date="2025-03-01",
        downloaded_at="2026-10-16",
        transformation="none",
        missing_flag="false",
        notes="Test fixture; not a real observation.",
    )
    result.update(overrides)
    return result


def test_valid_observation_is_normalized():
    result = validate_observation_rows([observation(year="02024", value="2.5e-2")])
    assert result[0]["year"] == "2024"
    assert float(result[0]["value"]) == pytest.approx(0.025)


def test_missing_observation_must_have_blank_value():
    with pytest.raises(ValueError, match="missing observations must have blank value"):
        validate_observation_rows([observation(missing_flag="true")])


def test_missing_observation_can_be_recorded_explicitly():
    result = validate_observation_rows([
        observation(value="", missing_flag="true")
    ])
    assert result[0]["value"] == ""
    assert result[0]["missing_flag"] == "true"


@pytest.mark.parametrize("value", ["not-a-number", "nan", "inf", "-inf"])
def test_invalid_numeric_values_are_rejected(value):
    with pytest.raises(ValueError, match="value"):
        validate_observation_rows([observation(value=value)])


def test_non_missing_observation_requires_value():
    with pytest.raises(ValueError, match="require value"):
        validate_observation_rows([observation(value="")])


def test_year_must_be_positive_integer():
    with pytest.raises(ValueError, match="year"):
        validate_observation_rows([observation(year="0")])


def test_duplicate_series_key_is_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        validate_observation_rows([observation(), observation(notes="duplicate")])


def test_distinct_series_codes_can_coexist():
    result = validate_observation_rows([
        observation(source_series_code="SERIES-A"),
        observation(source_series_code="SERIES-B"),
    ])
    assert len(result) == 2


def test_missing_flag_must_be_boolean():
    with pytest.raises(ValueError, match="missing_flag"):
        validate_observation_rows([observation(missing_flag="unknown")])
