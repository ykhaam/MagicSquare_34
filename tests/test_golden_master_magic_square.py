"""GM-2 — Golden Master per-scenario regression tests (approve pattern)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from control.puzzle_solver import solution
from tests.golden_master.approve import (
    approve_golden_master,
    approve_section,
    build_golden_master_content,
    format_scenario_block,
)
from tests.golden_master.contracts import (
    assert_error_contract,
    assert_int6_output,
    assert_one_index_coordinates,
    assert_reverse_fallback_combination,
    assert_row_major_blank_order,
    assert_small_first_combination,
)
from tests.golden_master.scenarios import GM2_SCENARIOS, GoldenMasterScenario

EXPECTED_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"


@pytest.fixture
def solve() -> Callable[[list[list[int]]], list[int] | ErrorResponse]:
    """Boundary solve entrypoint under test (API result serialization)."""
    return UIBoundary(execute=solution).solve


def _assert_contracts(
    scenario: GoldenMasterScenario,
    result: list[int] | ErrorResponse,
) -> None:
    """Verify Report 02 contract rules for one golden master scenario."""
    if scenario.kind == "success":
        assert isinstance(result, list)
        assert_int6_output(result)
        assert_one_index_coordinates(result)
        assert_row_major_blank_order(scenario.grid, result)
        if scenario.section == "normal_success":
            assert_small_first_combination(scenario.grid, result)
        if scenario.section == "reverse_success":
            assert_reverse_fallback_combination(scenario.grid, result)
        return

    assert scenario.expected_error_code is not None
    assert isinstance(result, ErrorResponse)
    assert_error_contract(result, scenario.expected_error_code)


def _run_golden_master_case(
    solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    scenario: GoldenMasterScenario,
) -> None:
    """Execute one GM-TC scenario: contract checks + section approve."""
    result = solve(scenario.grid)
    _assert_contracts(scenario, result)

    actual_block = format_scenario_block(scenario.section, scenario.grid, result)
    full_content = build_golden_master_content(solve)
    reason = approve_section(
        scenario.section,
        actual_block,
        EXPECTED_PATH,
        full_content,
        auto_create=True,
    )
    if reason is not None:
        pytest.fail(reason)


@pytest.mark.golden_master
class TestGoldenMasterMagicSquare:
    """[TAG][GoldenMaster] — GM-TC-01~05 solver output vs baseline."""

    def test_gm_tc_01_normal_success(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-TC-01 — Step A (small-first) success; int[6] row-major 1-index."""
        _run_golden_master_case(solve, GM2_SCENARIOS[0])

    def test_gm_tc_02_reverse_success(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-TC-02 — Step B reverse fallback success."""
        _run_golden_master_case(solve, GM2_SCENARIOS[1])

    def test_gm_tc_03_invalid_blank_count(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-TC-03 — INVALID_BLANK_COUNT (UI_INVALID_EMPTY_COUNT contract)."""
        _run_golden_master_case(solve, GM2_SCENARIOS[2])

    def test_gm_tc_04_duplicate_number(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-TC-04 — DUPLICATE_NUMBER (UI_DUPLICATE_VALUE contract)."""
        _run_golden_master_case(solve, GM2_SCENARIOS[3])

    def test_gm_tc_05_no_valid_magic_square(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-TC-05 — NO_VALID_MAGIC_SQUARE (DOMAIN_NO_SOLUTION contract)."""
        _run_golden_master_case(solve, GM2_SCENARIOS[4])

    def test_gm_tc_all_sections_full_baseline(
        self,
        solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    ) -> None:
        """GM-2 — full golden_master_expected.txt regression (GM-1 aggregate)."""
        actual = build_golden_master_content(solve)
        reason = approve_golden_master(actual, EXPECTED_PATH, auto_create=False)
        if reason is not None:
            pytest.fail(reason)
