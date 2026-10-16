"""Validation utilities for the versioned Genuine Nations roster.

This module validates metadata and provenance; it does not decide which entities
belong in the researcher's theory-defined sample.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

REQUIRED_ROSTER_COLUMNS = (
    "entity_id",
    "entity_name",
    "cohort",
    "nuclear_set_member",
    "aaa_set_member",
    "credit_rating_agency",
    "rating_reference_date",
    "inclusion_rule",
    "evidence_source",
    "evidence_accessed_date",
    "membership_status",
    "notes",
)
VALID_COHORTS = {"primary", "sensitivity"}
VALID_BOOLEAN_STRINGS = {"true", "false"}
VALID_MEMBERSHIP_STATUSES = {"proposed", "verified", "excluded", "disputed"}


def validate_roster_rows(
    rows: Iterable[dict[str, str]],
    *,
    expected_primary_count: int | None = None,
    expected_sensitivity_count: int | None = None,
) -> list[dict[str, str]]:
    """Validate roster rows and return normalized copies.

    Counts are optional because an incomplete working roster must remain
    inspectable. Set them when validating a frozen release.
    """
    normalized: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for line_number, raw in enumerate(rows, start=2):
        row = {key: (value or "").strip() for key, value in raw.items()}
        missing_columns = [key for key in REQUIRED_ROSTER_COLUMNS if key not in row]
        if missing_columns:
            raise ValueError(
                f"Row {line_number}: missing columns {missing_columns}"
            )

        for field in ("entity_id", "entity_name", "cohort", "membership_status"):
            if not row[field]:
                raise ValueError(f"Row {line_number}: {field} is required")

        if row["cohort"] not in VALID_COHORTS:
            raise ValueError(
                f"Row {line_number}: cohort must be one of {sorted(VALID_COHORTS)}"
            )
        if row["membership_status"] not in VALID_MEMBERSHIP_STATUSES:
            raise ValueError(
                f"Row {line_number}: membership_status must be one of "
                f"{sorted(VALID_MEMBERSHIP_STATUSES)}"
            )

        for field in ("nuclear_set_member", "aaa_set_member"):
            row[field] = row[field].lower()
            if row[field] not in VALID_BOOLEAN_STRINGS:
                raise ValueError(
                    f"Row {line_number}: {field} must be 'true' or 'false'"
                )

        key = (row["entity_id"], row["cohort"])
        if key in seen:
            raise ValueError(
                f"Row {line_number}: duplicate entity_id/cohort pair {key}"
            )
        seen.add(key)

        if row["membership_status"] == "verified":
            for field in ("inclusion_rule", "evidence_source", "evidence_accessed_date"):
                if not row[field]:
                    raise ValueError(
                        f"Row {line_number}: verified entries require {field}"
                    )
            if row["aaa_set_member"] == "true" and not row["credit_rating_agency"]:
                raise ValueError(
                    f"Row {line_number}: AAA membership requires credit_rating_agency"
                )
            if row["aaa_set_member"] == "true" and not row["rating_reference_date"]:
                raise ValueError(
                    f"Row {line_number}: AAA membership requires rating_reference_date"
                )

        normalized.append(row)

    counts = {
        cohort: sum(row["cohort"] == cohort for row in normalized)
        for cohort in VALID_COHORTS
    }
    for cohort, expected in (
        ("primary", expected_primary_count),
        ("sensitivity", expected_sensitivity_count),
    ):
        if expected is not None and counts[cohort] != expected:
            raise ValueError(
                f"Expected {expected} {cohort} rows; found {counts[cohort]}"
            )
    return normalized


def load_roster_csv(
    path: str | Path,
    *,
    expected_primary_count: int | None = None,
    expected_sensitivity_count: int | None = None,
) -> list[dict[str, str]]:
    """Load and validate a UTF-8 CSV roster."""
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Roster CSV has no header")
        missing = [c for c in REQUIRED_ROSTER_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Roster CSV missing required columns: {missing}")
        return validate_roster_rows(
            reader,
            expected_primary_count=expected_primary_count,
            expected_sensitivity_count=expected_sensitivity_count,
        )
