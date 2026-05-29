"""Boundary input validation RED skeletons — U-IN-04~08 (Report/07 §5.1)."""

from __future__ import annotations

import pytest

from boundary.input_validator import InputValidator


class TestUIn04Through08InputValidation:
    """U-IN-04~08: value range and duplicate checks (InputValidator)."""

    def test_u_in_04_minus_one_returns_e004(self) -> None:
        """U-IN-04a — cell -1 triggers E004 / UI_INVALID_VALUE_RANGE."""
        # Given
        # matrix = valid 4x4 with one cell set to -1

        # When
        # result = validator.validate(matrix)

        pytest.fail("RED: U-IN-04 — 셀 -1 → E004 범위 위반")

    def test_u_in_05_seventeen_returns_e004(self) -> None:
        """U-IN-04b — RD-06 value 17 triggers E004."""
        # Given
        # matrix = PRD RD-06 invalid range grid

        # When
        # result = validator.validate(matrix)

        pytest.fail("RED: U-IN-05 — RD-06 값 17 → E004 범위 위반")

    def test_u_in_06_duplicate_nonzero_returns_e005(self) -> None:
        """U-IN-05 — RD-05 duplicate non-zero triggers E005."""
        # Given
        # matrix = PRD RD-05 duplicate value grid

        # When
        # result = validator.validate(matrix)

        pytest.fail("RED: U-IN-06 — RD-05 non-zero 중복 → E005")

    def test_u_in_07_out_of_range_ninety_nine_returns_e004(self) -> None:
        """U-IN extension — value 99 in cell triggers E004 (Report/02 UT-E04)."""
        # Given
        # matrix = valid 4x4 with one cell set to 99

        # When
        # result = validator.validate(matrix)

        pytest.fail("RED: U-IN-07 — 셀 99 → E004 범위 위반")

    def test_u_in_08_non_list_grid_returns_e001(self) -> None:
        """U-IN extension — non-list grid type triggers E001 (PRD EX-05)."""
        # Given
        # matrix = "not_a_grid"

        # When
        # result = validator.validate(matrix)

        pytest.fail("RED: U-IN-08 — 비-list 입력 → E001 size 거부")
