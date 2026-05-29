"""Additional magic_validator branches for coverage."""

from __future__ import annotations

from entity.services.magic_validator import is_magic_square


class TestMagicValidatorBranches:
    """Edge grids for is_magic_square false branches."""

    def test_wrong_row_count_returns_false(self) -> None:
        """Fewer than four rows is not magic."""
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        assert is_magic_square(grid) is False

    def test_ragged_row_returns_false(self) -> None:
        """Ragged rows are not magic."""
        grid = [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

        assert is_magic_square(grid) is False

    def test_incomplete_values_set_returns_false(self) -> None:
        """Missing values from 1..16 are not magic."""
        grid = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        assert is_magic_square(grid) is False

    def test_value_below_min_returns_false(self) -> None:
        """Values below 1 fail validation."""
        grid = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        assert is_magic_square(grid) is False

    def test_value_above_max_returns_false(self) -> None:
        """Values above 16 fail validation."""
        grid = [
            [17, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        assert is_magic_square(grid) is False
