"""Entity logic — D-MIS-01 (find_not_exist_nums)."""

from __future__ import annotations

from entity.services.missing_number_finder import find_not_exist_nums
from tests.entity.conftest import G1


class TestDMis01MissingNumbers:
    """D-MIS-01 — missing numbers on G1 (no Domain Mock)."""

    def test_d_mis_01_g1_missing_sorted(self) -> None:
        """D-MIS-01 — G1 missing set {7,10} ascending."""
        # Given
        grid = G1

        # When
        missing = find_not_exist_nums(grid)

        # Then
        assert missing == [7, 10]
