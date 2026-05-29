"""Shared constants for AC-FR-01-01 boundary input validation tests."""

from __future__ import annotations

AC_FR_01_01 = "AC-FR-01-01"

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

IN_SCOPE_SCENARIO_TAGS: frozenset[str] = frozenset(
    {"null", "empty_list", "four_empty_rows", "size_3x4"}
)

FORBIDDEN_SCENARIO_TAGS: frozenset[str] = frozenset(
    {
        "empty_count",
        "value_range",
        "duplicate",
        "domain_no_solution",
        "success_output",
    }
)

EXCLUDED_AC_IDS: frozenset[str] = frozenset(
    {
        "AC-FR-01-02",
        "AC-FR-01-03",
        "AC-FR-01-04",
        "AC-FR-01-05",
    }
)

EXCLUDED_FR_IDS: frozenset[str] = frozenset(
    {
        "FR-02",
        "FR-03",
        "FR-04",
        "FR-05",
    }
)
