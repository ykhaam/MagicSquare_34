"""Data layer tests — DATA-T01~T05 (InMemory repositories)."""

from __future__ import annotations

import pytest

from data.exceptions import DataInvalidGridError, DataNotFoundError
from data.matrix_repository import InMemoryMatrixRepository, InMemoryResultRepository
from tests.entity.conftest import G1_RD01


class TestInMemoryMatrixRepository:
    """DATA-T01, T02, T04 — matrix save/load contract."""

    def test_data_t01_save_and_load_round_trip(self) -> None:
        """DATA-T01 — save then load returns identical grid."""
        repo = InMemoryMatrixRepository()
        grid = G1_RD01

        repo.save("puzzle-1", grid)
        loaded = repo.load("puzzle-1")

        assert loaded == grid
        assert loaded is not grid
        assert loaded[0] is not grid[0]

    def test_data_t02_load_missing_id_raises_not_found(self) -> None:
        """DATA-T02 — unknown id raises DATA_NOT_FOUND."""
        repo = InMemoryMatrixRepository()

        with pytest.raises(DataNotFoundError) as exc_info:
            repo.load("missing")

        assert exc_info.value.code == "DATA_NOT_FOUND"

    def test_data_t04_invalid_grid_rejected_on_save(self) -> None:
        """DATA-T04 — invalid grid cannot be stored."""
        repo = InMemoryMatrixRepository()

        with pytest.raises(DataInvalidGridError):
            repo.save("bad", [[1, 2, 3]])


class TestInMemoryResultRepository:
    """DATA-T05 — optional result save/load."""

    def test_data_t05_result_save_and_load(self) -> None:
        """DATA-T05 — six-element result round trip."""
        repo = InMemoryResultRepository()
        payload = [2, 2, 7, 3, 3, 10]

        repo.save("result-1", payload)

        assert repo.load("result-1") == payload
