"""In-memory matrix and result repositories."""

from __future__ import annotations

from data.exceptions import DataInvalidGridError, DataInvalidIdError, DataNotFoundError
from entity.grid_validator import is_valid_structure


class InMemoryMatrixRepository:
    """Process-local storage for 4×4 grids keyed by string id."""

    def __init__(self) -> None:
        """Initialize an empty store."""
        self._store: dict[str, list[list[int]]] = {}

    def save(self, grid_id: str, grid: list[list[int]]) -> None:
        """Persist a validated 4×4 grid.

        Args:
            grid_id: Non-empty identifier.
            grid: Valid puzzle matrix.

        Raises:
            DataInvalidIdError: When id is blank.
            DataInvalidGridError: When grid structure is invalid.
        """
        if not grid_id or not grid_id.strip():
            raise DataInvalidIdError()
        if not is_valid_structure(grid):
            raise DataInvalidGridError()
        self._store[grid_id] = [row[:] for row in grid]

    def load(self, grid_id: str) -> list[list[int]]:
        """Load a stored grid copy.

        Args:
            grid_id: Identifier used during save.

        Returns:
            Deep copy of the stored grid.

        Raises:
            DataInvalidIdError: When id is blank.
            DataNotFoundError: When id is unknown.
        """
        if not grid_id or not grid_id.strip():
            raise DataInvalidIdError()
        if grid_id not in self._store:
            raise DataNotFoundError()
        stored = self._store[grid_id]
        return [row[:] for row in stored]


class InMemoryResultRepository:
    """Process-local storage for six-element solve vectors."""

    def __init__(self) -> None:
        """Initialize an empty store."""
        self._store: dict[str, list[int]] = {}

    def save(self, result_id: str, result: list[int]) -> None:
        """Persist a solve result vector."""
        from data.exceptions import DataInvalidIdError, DataInvalidResultError

        if not result_id or not result_id.strip():
            raise DataInvalidIdError()
        if len(result) != 6:
            raise DataInvalidResultError()
        self._store[result_id] = result[:]

    def load(self, result_id: str) -> list[int]:
        """Load a stored result vector."""
        from data.exceptions import DataInvalidIdError, DataNotFoundError

        if not result_id or not result_id.strip():
            raise DataInvalidIdError()
        if result_id not in self._store:
            raise DataNotFoundError()
        return self._store[result_id][:]
