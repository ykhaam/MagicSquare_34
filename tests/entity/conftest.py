"""Entity-track fixtures — G0~G3 and validation variants."""

from __future__ import annotations

import pytest

G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G2: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 0],
]

G3: list[list[int]] = [
    [11, 15, 0, 6],
    [2, 10, 3, 4],
    [12, 0, 14, 8],
    [9, 5, 1, 7],
]

G0_ROW: list[list[int]] = [
    [16, 3, 2, 14],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G0_COL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 9],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G0_DIAG: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 2],
]

G0_DUP: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 16],
]

G0_ZERO: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]

G1_RD01: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 1],
]

RD_04: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 0, 1],
]

RD_05: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 16, 0],
]

RD_06: list[list[int]] = [
    [16, 0, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 17, 0],
]


@pytest.fixture
def grid_g0() -> list[list[int]]:
    """Complete magic square G0."""
    return [row[:] for row in G0]


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """Partial grid G1 with blanks at (2,2) and (3,3)."""
    return [row[:] for row in G1]


@pytest.fixture
def grid_g2() -> list[list[int]]:
    """Partial grid G2 for Step B success."""
    return [row[:] for row in G2]


@pytest.fixture
def grid_g3() -> list[list[int]]:
    """Unsolvable grid G3."""
    return [row[:] for row in G3]
