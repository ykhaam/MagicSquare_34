"""Structural validation for magic-square grids at the entity layer."""

from __future__ import annotations

from typing import Any

from entity.constants import (
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_EMPTY_COUNT,
)


def is_valid_structure(raw: Any) -> bool:
    """Return True when raw satisfies D-STRUCT-01~04."""
    if not isinstance(raw, list):
        return False
    if len(raw) != GRID_SIZE:
        return False
    empty_count = 0
    seen: set[int] = set()
    for row in raw:
        if not isinstance(row, list) or len(row) != GRID_SIZE:
            return False
        for value in row:
            if not isinstance(value, int):
                return False
            if value == EMPTY_CELL_VALUE:
                empty_count += 1
                continue
            if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                return False
            if value in seen:
                return False
            seen.add(value)
    return empty_count == REQUIRED_EMPTY_COUNT
