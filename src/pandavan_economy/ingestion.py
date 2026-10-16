"""Schema and type checks for long-form country-year observations."""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

OBSERVATION_COLUMNS = (
    "entity_id",
    "entity_name",
    "year",
    "variable_name",
    "value",
    "unit",
    "source",
    "source_series_code",
    "frequency",
    "reference_period",
    "source_release_date",
    "downloaded_at",
    "transformation",
    "missing_flag",
    "notes",
)
BOOLEAN_STRINGS = {"true", "false"}


def validate_observation_rows(
    rows: Iterable[dict[str, str]],
) -> list[dict[str, str]]:
    """Validate long-form observations without imputing or transforming data."""
    validated: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()

    for line_number, raw in enumerate(rows, start=2):
        row = {key: (value or "").strip() for key, value in raw.items()}
        missing_columns = [key for key in OBSERVATION_COLUMNS if key not in row]
        if missing_columns:
            raise ValueError(
                f"Row {line_number}: missing columns {missing_columns}"
            )

        for field in ("entity_id", "entity_name", "year", "variable_name",
                      "unit", "source", "frequency", "missing_flag"):
            if not row[field]:
                raise ValueError(f"Row {line_number}: {field} is required")

        try:
            year = int(row["year"])
        except ValueError as exc:
            raise ValueError(f"Row {line_number}: year must be an integer") from exc
        if year < 1:
            raise ValueError(f"Row {line_number}: year must be positive")
        row["year"] = str(year)

        row["missing_flag"] = row["missing_flag"].lower()
        if row["missing_flag"] not in BOOLEAN_STRINGS:
            raise ValueError(
                f"Row {line_number}: missing_flag must be 'true' or 'false'"
            )
        if row["missing_flag"] == "true":
            if row["value"]:
                raise ValueError(
                    f"Row {line_number}: missing observations must have blank value"
                )
        else:
            if not row["value"]:
                raise ValueError(
                    f"Row {line_number}: non-missing observations require value"
                )
            try:
                value = float(row["value"])
            except ValueError as exc:
                raise ValueError(
                    f"Row {line_number}: value must be numeric"
                ) from exc
            if not math.isfinite(value):
                raise ValueError(
                    f"Row {line_number}: value must be finite"
                )
            row["value"] = repr(value)

        key = (
            row["entity_id"],
            row["year"],
            row["variable_name"],
            row["source_series_code"],
        )
        if key in seen:
            raise ValueError(
                f"Row {line_number}: duplicate entity/year/variable/source-series key {key}"
            )
        seen.add(key)
        validated.append(row)

    return validated


def load_observations_csv(path: str | Path) -> list[dict[str, str]]:
    """Load and validate a UTF-8 long-form observation CSV."""
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Observation CSV has no header")
        missing = [c for c in OBSERVATION_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Observation CSV missing required columns: {missing}")
        return validate_observation_rows(reader)
