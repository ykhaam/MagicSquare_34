"""Golden Master contract assertions (Report 02 public contract)."""

from __future__ import annotations

from boundary.schemas import ErrorResponse
from entity.services.blank_locator import find_blank_coords
from entity.services.missing_number_finder import find_not_exist_nums


def assert_int6_output(result: list[int]) -> None:
    """Success vector is length 6 with integer elements."""
    assert isinstance(result, list)
    assert len(result) == 6
    assert all(isinstance(value, int) for value in result)


def assert_one_index_coordinates(result: list[int]) -> None:
    """Coordinates in the success vector are 1-indexed within the 4×4 grid."""
    r1, c1, _n1, r2, c2, _n2 = result
    for coord in (r1, c1, r2, c2):
        assert 1 <= coord <= 4


def assert_row_major_blank_order(grid: list[list[int]], result: list[int]) -> None:
    """Placement targets follow row-major blank order (first blank, then second)."""
    first, second = find_blank_coords(grid)
    r1, c1, _n1, r2, c2, _n2 = result
    assert (r1, c1) == first
    assert (r2, c2) == second


def assert_small_first_combination(grid: list[list[int]], result: list[int]) -> None:
    """Step A places the smaller missing value in the first blank."""
    missing = find_not_exist_nums(grid)
    small, large = missing[0], missing[1]
    _r1, _c1, n1, _r2, _c2, n2 = result
    assert n1 == small
    assert n2 == large


def assert_reverse_fallback_combination(grid: list[list[int]], result: list[int]) -> None:
    """Step B places the larger missing value in the first blank (reverse order)."""
    missing = find_not_exist_nums(grid)
    small, large = missing[0], missing[1]
    _r1, _c1, n1, _r2, _c2, n2 = result
    assert n1 == large
    assert n2 == small


def assert_error_contract(result: ErrorResponse, expected_code: str) -> None:
    """Error payload exposes a stable code and non-empty fixed message."""
    assert isinstance(result, ErrorResponse)
    assert result.code == expected_code
    assert isinstance(result.message, str)
    assert len(result.message) > 0
