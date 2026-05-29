"""Domain structure tests — DT-E01~E07 (MagicGrid.from_raw)."""

from __future__ import annotations

import pytest

from control.solve_partial_magic_square import solution
from entity.exceptions import DomainInvalidGridError, UnsolvableDomainError
from entity.magic_grid import MagicGrid
from tests.entity.conftest import G3, RD_04, RD_05, RD_06


THREE_BY_THREE: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

THREE_BLANKS: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 0, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 1],
]

MINUS_ONE_CELL: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, -1, 14, 0],
]

DUPLICATE_SEVEN: list[list[int]] = [
    [7, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 16, 0],
]


class TestMagicGridFromRaw:
    """DT-E01~E06 — MagicGrid.from_raw rejects invalid structure."""

    def test_dt_e01_invalid_size_3x3(self) -> None:
        """DT-E01 — 3×3 grid raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError) as exc_info:
            MagicGrid.from_raw(THREE_BY_THREE)
        assert exc_info.value.code == "DOMAIN_INVALID_GRID"

    def test_dt_e02_single_empty_cell(self) -> None:
        """DT-E02 — one empty cell raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError):
            MagicGrid.from_raw(RD_04)

    def test_dt_e03_three_empty_cells(self) -> None:
        """DT-E03 — three empty cells raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError):
            MagicGrid.from_raw(THREE_BLANKS)

    def test_dt_e04_value_seventeen(self) -> None:
        """DT-E04 — value 17 raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError):
            MagicGrid.from_raw(RD_06)

    def test_dt_e05_value_minus_one(self) -> None:
        """DT-E05 — value -1 raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError):
            MagicGrid.from_raw(MINUS_ONE_CELL)

    def test_dt_e06_duplicate_nonzero(self) -> None:
        """DT-E06 — duplicate non-zero raises DOMAIN_INVALID_GRID."""
        with pytest.raises(DomainInvalidGridError):
            MagicGrid.from_raw(DUPLICATE_SEVEN)

    def test_dt_e07_no_solution_after_valid_from_raw(self) -> None:
        """DT-E07 — valid grid with no completion raises DOMAIN_NO_SOLUTION."""
        MagicGrid.from_raw(G3)
        with pytest.raises(UnsolvableDomainError) as exc_info:
            solution(G3)
        assert exc_info.value.code == "DOMAIN_NO_SOLUTION"
