"""Golden master scenario grids — GM-1 baseline / GM-2 test cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from boundary.error_codes import DUPLICATE_VALUE_CODE, INVALID_EMPTY_COUNT_CODE
from entity.exceptions import DOMAIN_NO_SOLUTION_CODE
from tests.entity.conftest import G0, G1_RD01, G2, G3, RD_05

NORMAL_SUCCESS_GRID: list[list[int]] = G1_RD01
REVERSE_SUCCESS_GRID: list[list[int]] = G2
INVALID_BLANK_COUNT_GRID: list[list[int]] = G0
DUPLICATE_NUMBER_GRID: list[list[int]] = RD_05
NO_VALID_SOLUTION_GRID: list[list[int]] = G3


@dataclass(frozen=True)
class GoldenMasterScenario:
    """One golden master scenario keyed by section name in the baseline file."""

    test_id: str
    section: str
    grid: list[list[int]]
    kind: Literal["success", "error"]
    expected_error_code: str | None = None


GM2_SCENARIOS: tuple[GoldenMasterScenario, ...] = (
    GoldenMasterScenario(
        "GM-TC-01",
        "normal_success",
        NORMAL_SUCCESS_GRID,
        "success",
    ),
    GoldenMasterScenario(
        "GM-TC-02",
        "reverse_success",
        REVERSE_SUCCESS_GRID,
        "success",
    ),
    GoldenMasterScenario(
        "GM-TC-03",
        "invalid_blank_count",
        INVALID_BLANK_COUNT_GRID,
        "error",
        INVALID_EMPTY_COUNT_CODE,
    ),
    GoldenMasterScenario(
        "GM-TC-04",
        "duplicate_number",
        DUPLICATE_NUMBER_GRID,
        "error",
        DUPLICATE_VALUE_CODE,
    ),
    GoldenMasterScenario(
        "GM-TC-05",
        "no_valid_solution",
        NO_VALID_SOLUTION_GRID,
        "error",
        DOMAIN_NO_SOLUTION_CODE,
    ),
)

GM1_SCENARIOS: tuple[GoldenMasterScenario, ...] = GM2_SCENARIOS
