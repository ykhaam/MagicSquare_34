"""Boundary flow isolation — U-FLOW-02 (invalid inputs skip execute)."""

from __future__ import annotations

from unittest.mock import Mock

from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from tests.entity.conftest import RD_04, RD_05, RD_06


class TestUFlow02InvalidSkipsExecute:
    """U-FLOW-02 — invalid inputs must not call Control/Domain execute (0 times)."""

    def test_u_flow_02_null_matrix_skips_execute(self) -> None:
        """U-FLOW-02a — null matrix: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)
        matrix = None

        # When
        result = boundary.solve(matrix)

        # Then
        assert isinstance(result, ErrorResponse)
        mock_execute.assert_not_called()
        assert mock_execute.call_count == 0

    def test_u_flow_02_invalid_size_skips_execute(self) -> None:
        """U-FLOW-02b — invalid size: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)
        matrix: list[list[int]] = []

        # When
        boundary.solve(matrix)

        # Then
        mock_execute.assert_not_called()

    def test_u_flow_02_invalid_empty_count_skips_execute(self) -> None:
        """U-FLOW-02c — empty count != 2: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)

        # When
        boundary.solve(RD_04)

        # Then
        mock_execute.assert_not_called()

    def test_u_flow_02_invalid_range_skips_execute(self) -> None:
        """U-FLOW-02d — value range violation: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)

        # When
        boundary.solve(RD_06)

        # Then
        mock_execute.assert_not_called()

    def test_u_flow_02_duplicate_skips_execute(self) -> None:
        """U-FLOW-02e — duplicate non-zero: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)

        # When
        boundary.solve(RD_05)

        # Then
        mock_execute.assert_not_called()

    def test_u_flow_02_ragged_grid_skips_execute(self) -> None:
        """U-FLOW-02f — ragged 4 rows: Failure; execute call_count==0."""
        # Given
        mock_execute = Mock(name="execute")
        boundary = UIBoundary(execute=mock_execute)
        matrix: list[list[int]] = [[]] * 4

        # When
        boundary.solve(matrix)

        # Then
        mock_execute.assert_not_called()
