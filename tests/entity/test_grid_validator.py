"""Entity structure validation — D-STRUCT SSOT (grid_validator)."""

from __future__ import annotations

from entity.grid_validator import (
    STRUCTURE_DUPLICATE_VALUE,
    STRUCTURE_INVALID_EMPTY_COUNT,
    STRUCTURE_INVALID_SIZE,
    STRUCTURE_INVALID_VALUE_RANGE,
    is_valid_structure,
    structure_failure_kind,
)
from tests.entity.conftest import G1, RD_05, RD_06


class TestGridValidatorStructure:
    """structure_failure_kind and is_valid_structure (shared with Boundary)."""

    def test_valid_g1_structure(self) -> None:
        """G1 satisfies D-STRUCT-01~04."""
        assert structure_failure_kind(G1) is None
        assert is_valid_structure(G1) is True

    def test_invalid_size_empty_list(self) -> None:
        """Empty list is invalid size."""
        assert structure_failure_kind([]) == STRUCTURE_INVALID_SIZE

    def test_invalid_empty_count(self) -> None:
        """RD-04 has one empty cell."""
        from tests.entity.conftest import RD_04

        assert structure_failure_kind(RD_04) == STRUCTURE_INVALID_EMPTY_COUNT

    def test_invalid_value_range(self) -> None:
        """RD-06 has value 17."""
        assert structure_failure_kind(RD_06) == STRUCTURE_INVALID_VALUE_RANGE

    def test_non_integer_cell(self) -> None:
        """Non-int cells are value-range violations."""
        grid = [[1.5, 0, 3, 13], [5, 11, 10, 8], [9, 7, 6, 12], [4, 14, 0, 1]]
        assert structure_failure_kind(grid) == STRUCTURE_INVALID_VALUE_RANGE

    def test_duplicate_nonzero(self) -> None:
        """RD-05 duplicate non-zero values."""
        assert structure_failure_kind(RD_05) == STRUCTURE_DUPLICATE_VALUE
