"""Boundary input validation — U-IN-04~08 (value range, duplicate, type)."""

from __future__ import annotations

from boundary.error_codes import (
    DUPLICATE_VALUE_CODE,
    E004_CODE,
    E005_CODE,
    INVALID_SIZE_CODE,
    INVALID_VALUE_RANGE_MESSAGE,
)
from boundary.input_validator import InputValidator
from tests.entity.conftest import RD_05, RD_06


class TestUIn04Through08InputValidation:
    """U-IN-04~08: value range and duplicate checks (InputValidator)."""

    def test_u_in_04_minus_one_returns_e004(self) -> None:
        """U-IN-04a — cell -1 triggers E004 / UI_INVALID_VALUE_RANGE."""
        # Given
        matrix = [
            [16, 0, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, -1, 14, 0],
        ]
        validator = InputValidator()

        # When
        result = validator.validate(matrix)

        # Then
        assert result is not None
        assert result.error.code == E004_CODE
        assert result.error.message == INVALID_VALUE_RANGE_MESSAGE

    def test_u_in_05_seventeen_returns_e004(self) -> None:
        """U-IN-04b — RD-06 value 17 triggers E004."""
        # Given
        validator = InputValidator()

        # When
        result = validator.validate(RD_06)

        # Then
        assert result is not None
        assert result.error.code == E004_CODE

    def test_u_in_06_duplicate_nonzero_returns_e005(self) -> None:
        """U-IN-05 — RD-05 duplicate non-zero triggers E005."""
        # Given
        validator = InputValidator()

        # When
        result = validator.validate(RD_05)

        # Then
        assert result is not None
        assert result.error.code == E005_CODE
        assert result.error.code == DUPLICATE_VALUE_CODE

    def test_u_in_07_out_of_range_ninety_nine_returns_e004(self) -> None:
        """U-IN extension — value 99 in cell triggers E004 (Report/02 UT-E04)."""
        # Given
        matrix = [
            [16, 0, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 99, 0],
        ]
        validator = InputValidator()

        # When
        result = validator.validate(matrix)

        # Then
        assert result is not None
        assert result.error.code == E004_CODE

    def test_u_in_08_non_list_grid_returns_e001(self) -> None:
        """U-IN extension — non-list grid type triggers E001 (PRD EX-05)."""
        # Given
        validator = InputValidator()

        # When
        result = validator.validate("not_a_grid")

        # Then
        assert result is not None
        assert result.error.code == INVALID_SIZE_CODE
