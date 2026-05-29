"""Entity logic RED skeleton — D-LOC-01 (find_blank_coords)."""

from __future__ import annotations

import pytest

from entity.services.blank_locator import find_blank_coords


class TestDLoc01BlankCoords:
    """D-LOC-01 — row-major blank coordinates on G1 (no Domain Mock)."""

    def test_d_loc_01_g1_row_major_blanks(self) -> None:
        """D-LOC-01 — G1 blanks at (2,2) and (3,3) 1-index."""
        # Given
        # grid = G1

        # When
        # first, second = find_blank_coords(grid)

        pytest.fail("RED: D-LOC-01 — G1 row-major 빈칸 (2,2),(3,3) 1-index")
