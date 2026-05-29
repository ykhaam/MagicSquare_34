"""Integration tests — IT-N01~N02, IT-E01~E02, IT-E04."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from boundary.error_codes import INVALID_EMPTY_COUNT_CODE, INVALID_SIZE_CODE
from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import solution
from data.matrix_repository import InMemoryMatrixRepository
from entity.exceptions import DOMAIN_NO_SOLUTION_CODE
from entity.services.magic_validator import is_magic_square
from tests.entity.conftest import G0, G1_RD01, G3, RD_04


class TestIntegrationHappyPath:
    """IT-N01~N02 — end-to-end solve and persistence."""

    def test_it_n01_boundary_to_domain_known_puzzle(self) -> None:
        """IT-N01 — UIBoundary + real solver returns int[6] magic completion."""
        boundary = UIBoundary(execute=solution)

        result = boundary.solve(G1_RD01)

        assert isinstance(result, list)
        assert len(result) == 6
        filled = [row[:] for row in G1_RD01]
        r1, c1, n1, r2, c2, n2 = result
        filled[r1 - 1][c1 - 1] = n1
        filled[r2 - 1][c2 - 1] = n2
        assert is_magic_square(filled)

    def test_it_n02_save_load_and_resolve_same_result(self) -> None:
        """IT-N02 — repository round trip preserves solve output."""
        repo = InMemoryMatrixRepository()
        repo.save("session-1", G1_RD01)
        loaded = repo.load("session-1")
        boundary = UIBoundary(execute=solution)

        first = boundary.solve(loaded)
        second = boundary.solve(loaded)

        assert first == second


class TestIntegrationFailures:
    """IT-E01~E04 — failure paths without Domain invocation where required."""

    def test_it_e01_invalid_size_skips_execute(self) -> None:
        """IT-E01 — 3×4 input returns INVALID_SIZE; execute not called."""
        mock_execute = Mock()
        boundary = UIBoundary(execute=mock_execute)
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        result = boundary.solve(grid)

        assert isinstance(result, ErrorResponse)
        assert result.code == INVALID_SIZE_CODE
        mock_execute.assert_not_called()

    def test_it_e02_unsolvable_returns_domain_no_solution(self) -> None:
        """IT-E02 — unsolvable puzzle maps to DOMAIN_NO_SOLUTION."""
        boundary = UIBoundary(execute=solution)

        result = boundary.solve(G3)

        assert isinstance(result, ErrorResponse)
        assert result.code == DOMAIN_NO_SOLUTION_CODE

    def test_it_e04_zero_empty_cells_returns_empty_count_error(self) -> None:
        """IT-E04 — complete grid (0 empties) rejected at Boundary."""
        mock_execute = Mock()
        boundary = UIBoundary(execute=mock_execute)
        complete = [row[:] for row in G0]

        result = boundary.solve(complete)

        assert isinstance(result, ErrorResponse)
        assert result.code == INVALID_EMPTY_COUNT_CODE
        mock_execute.assert_not_called()
