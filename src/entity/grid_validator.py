"""Structural validation for magic-square grids at the entity layer (D-STRUCT SSOT)."""

from __future__ import annotations

from typing import Any, Final

from entity.constants import (
    EMPTY_CELL_VALUE,
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
    REQUIRED_EMPTY_COUNT,
)

STRUCTURE_INVALID_SIZE: Final[str] = "invalid_size"
STRUCTURE_INVALID_EMPTY_COUNT: Final[str] = "invalid_empty_count"
STRUCTURE_INVALID_VALUE_RANGE: Final[str] = "invalid_value_range"
STRUCTURE_DUPLICATE_VALUE: Final[str] = "duplicate_value"


def structure_failure_kind(raw: Any) -> str | None:
    """Return a structure violation kind, or None when D-STRUCT-01~04 hold.

    Args:
        raw: Candidate 4×4 grid.

    Returns:
        One of ``STRUCTURE_*`` constants, or None when valid.
    """
    if raw is None or not isinstance(raw, list) or len(raw) != GRID_SIZE:
        return STRUCTURE_INVALID_SIZE

    empty_count = 0
    seen: set[int] = set()
    for row in raw:
        if not isinstance(row, list) or len(row) != GRID_SIZE:
            return STRUCTURE_INVALID_SIZE
        for value in row:
            if not isinstance(value, int):
                return STRUCTURE_INVALID_VALUE_RANGE
            if value == EMPTY_CELL_VALUE:
                empty_count += 1
                continue
            if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
                return STRUCTURE_INVALID_VALUE_RANGE
            if value in seen:
                return STRUCTURE_DUPLICATE_VALUE
            seen.add(value)

    if empty_count != REQUIRED_EMPTY_COUNT:
        return STRUCTURE_INVALID_EMPTY_COUNT
    return None


def is_valid_structure(raw: Any) -> bool:
    """Return True when raw satisfies D-STRUCT-01~04."""
    return structure_failure_kind(raw) is None
