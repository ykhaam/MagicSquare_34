"""Magic-square grid entity."""

from __future__ import annotations

from dataclasses import dataclass

from entity.constants import GRID_SIZE
from entity.domain_codes import DOMAIN_INVALID_GRID_CODE, DOMAIN_INVALID_GRID_MESSAGE
from entity.exceptions import DomainInvalidGridError
from entity.grid_validator import is_valid_structure


@dataclass(frozen=True)
class MagicGrid:
    """Validated 4×4 magic-square grid."""

    cells: tuple[tuple[int, int, int, int], ...]

    @classmethod
    def from_raw(cls, raw: list[list[int]]) -> MagicGrid:
        """Create a MagicGrid when D-STRUCT-01~04 hold.

        Args:
            raw: Raw 4×4 integer matrix.

        Returns:
            Frozen MagicGrid instance.

        Raises:
            DomainInvalidGridError: When structure validation fails.
        """
        if not is_valid_structure(raw):
            raise DomainInvalidGridError(
                code=DOMAIN_INVALID_GRID_CODE,
                message=DOMAIN_INVALID_GRID_MESSAGE,
            )
        rows = tuple(
            (raw[row][0], raw[row][1], raw[row][2], raw[row][3])
            for row in range(GRID_SIZE)
        )
        return cls(cells=rows)

    def to_raw(self) -> list[list[int]]:
        """Return a mutable copy of the underlying matrix."""
        return [list(row) for row in self.cells]
