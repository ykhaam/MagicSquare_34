"""Entity logic — D-VAL-01~06 (is_magic_square)."""

from __future__ import annotations

from entity.services.magic_validator import is_magic_square
from tests.entity.conftest import G0, G0_COL, G0_DIAG, G0_DUP, G0_ROW, G0_ZERO


class TestDVal01Through06MagicValidation:
    """D-VAL-01~06 — magic square predicate (no Domain Mock)."""

    def test_d_val_01_g0_complete_magic_true(self) -> None:
        """D-VAL-01 — G0 complete grid returns true."""
        # Given
        grid = G0

        # When
        result = is_magic_square(grid)

        # Then
        assert result is True

    def test_d_val_02_row_sum_mismatch(self) -> None:
        """D-VAL-02 — G0-ROW variant returns false."""
        # Given
        grid = G0_ROW

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_03_col_sum_mismatch(self) -> None:
        """D-VAL-03 — G0-COL variant returns false."""
        # Given
        grid = G0_COL

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_04_diagonal_mismatch(self) -> None:
        """D-VAL-04 — G0-DIAG variant returns false."""
        # Given
        grid = G0_DIAG

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_05_duplicate_false(self) -> None:
        """D-VAL-05 — G0-DUP variant returns false."""
        # Given
        grid = G0_DUP

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False

    def test_d_val_06_zero_in_filled_false(self) -> None:
        """D-VAL-06 — G0-ZERO variant returns false."""
        # Given
        grid = G0_ZERO

        # When
        result = is_magic_square(grid)

        # Then
        assert result is False
