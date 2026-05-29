"""Control/Entity solution — D-SOL-01~04 (solution)."""

from __future__ import annotations

import pytest

from control.solve_partial_magic_square import solution
from entity.exceptions import UnsolvableDomainError
from tests.entity.conftest import G1, G2, G3


class TestDSol01Through04Solution:
    """D-SOL-01~04 — solution vector contract (no Domain Mock)."""

    def test_d_sol_01_g1_step_b_success(self) -> None:
        """D-SOL-01 — G1 Step B success vector [2,2,10,3,3,7]."""
        # Given
        grid = G1

        # When
        result = solution(grid)

        # Then
        assert result == [2, 2, 10, 3, 3, 7]

    def test_d_sol_02_g2_step_b_reverse(self) -> None:
        """D-SOL-02 — G2 Step B reverse success."""
        # Given
        grid = G2

        # When
        result = solution(grid)

        # Then
        assert result == [1, 2, 2, 4, 4, 1]

    def test_d_sol_03_g3_unsolvable(self) -> None:
        """D-SOL-03 — G3 raises UnsolvableDomainError."""
        # Given
        grid = G3

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solution(grid)

    def test_d_sol_04_output_contract(self) -> None:
        """D-SOL-04 — G1 output len 6 and 1-index coordinates."""
        # Given
        grid = G1

        # When
        result = solution(grid)

        # Then
        assert len(result) == 6
        r1, c1, _n1, r2, c2, _n2 = result
        for coord in (r1, c1, r2, c2):
            assert 1 <= coord <= 4
