"""MagicGrid round-trip — covers to_raw after from_raw."""

from __future__ import annotations

from entity.magic_grid import MagicGrid
from tests.entity.conftest import G1


class TestMagicGridToRaw:
    """MagicGrid.to_raw preserves cell values."""

    def test_to_raw_round_trip_matches_g1(self) -> None:
        """to_raw returns a mutable copy equal to the source grid."""
        grid = MagicGrid.from_raw(G1)

        assert grid.to_raw() == G1
