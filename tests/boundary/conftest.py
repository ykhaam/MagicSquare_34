"""Fixtures for AC-FR-01-01 boundary input validation tests."""

from __future__ import annotations

import pytest

THREE_BY_FOUR_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]


@pytest.fixture
def grid_none() -> None:
    """Explicit None grid (BV-01)."""
    return None


@pytest.fixture
def grid_empty_list() -> list[list[int]]:
    """Empty list — zero rows (BV-02)."""
    return []


@pytest.fixture
def grid_four_empty_rows() -> list[list[int]]:
    """Four rows with zero columns — ragged size (BV-03)."""
    return [[]] * 4


@pytest.fixture
def grid_3x4() -> list[list[int]]:
    """3×4 grid — row count mismatch (BV-04)."""
    return THREE_BY_FOUR_GRID
