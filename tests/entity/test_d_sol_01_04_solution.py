"""Control/Entity solution RED skeletons — D-SOL-01~04 (solution)."""

from __future__ import annotations

import pytest

from control.puzzle_solver import solution


class TestDSol01Through04Solution:
    """D-SOL-01~04 — solution vector contract (no Domain Mock)."""

    def test_d_sol_01_g1_step_a_success(self) -> None:
        """D-SOL-01 — G1 Step A success vector [2,2,7,3,3,10]."""
        # Given
        # grid = G1

        # When
        # result = solution(grid)

        pytest.fail("RED: D-SOL-01 — G1 Step A [2,2,7,3,3,10]")

    def test_d_sol_02_g2_step_b_reverse(self) -> None:
        """D-SOL-02 — G2 Step B reverse success (G2 TBD)."""
        # Given
        # grid = G2

        # When
        # result = solution(grid)

        pytest.fail("RED: D-SOL-02 — G2 TBD")

    def test_d_sol_03_g3_unsolvable(self) -> None:
        """D-SOL-03 — G3 raises UnsolvableDomainError."""
        # Given
        # grid = G3

        # When / Then
        # with pytest.raises(UnsolvableDomainError):
        #     solution(grid)

        pytest.fail("RED: D-SOL-03 — G3 해 없음 UnsolvableDomainError")

    def test_d_sol_04_output_contract(self) -> None:
        """D-SOL-04 — G1 output len 6 and 1-index coordinates."""
        # Given
        # grid = G1

        # When
        # result = solution(grid)

        pytest.fail("RED: D-SOL-04 — 출력 len 6, 좌표 1-index")
