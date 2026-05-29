"""Boundary error codes and fixed messages (Report 02 §2.4)."""

from __future__ import annotations

from typing import Final

INVALID_SIZE_CODE: Final[str] = "UI_INVALID_SIZE"
INVALID_SIZE_MESSAGE: Final[str] = "Grid must be 4x4."

INVALID_EMPTY_COUNT_CODE: Final[str] = "UI_INVALID_EMPTY_COUNT"
INVALID_EMPTY_COUNT_MESSAGE: Final[str] = (
    "Grid must contain exactly 2 empty cells (0)."
)

INVALID_VALUE_RANGE_CODE: Final[str] = "UI_INVALID_VALUE_RANGE"
INVALID_VALUE_RANGE_MESSAGE: Final[str] = (
    "Cell values must be 0 or between 1 and 16."
)

DUPLICATE_VALUE_CODE: Final[str] = "UI_DUPLICATE_VALUE"
DUPLICATE_VALUE_MESSAGE: Final[str] = "Non-zero values must not duplicate."

UI_INTERNAL_CONTRACT_CODE: Final[str] = "UI_INTERNAL_CONTRACT"
UI_INTERNAL_CONTRACT_MESSAGE: Final[str] = (
    "Internal response contract violation."
)

# Report 07 E-code aliases (same contract as UI codes above)
E001_CODE: Final[str] = INVALID_SIZE_CODE
E002_CODE: Final[str] = INVALID_EMPTY_COUNT_CODE
E004_CODE: Final[str] = INVALID_VALUE_RANGE_CODE
E005_CODE: Final[str] = DUPLICATE_VALUE_CODE
E006_CODE: Final[str] = "DOMAIN_INVALID_GRID"
E007_CODE: Final[str] = "DOMAIN_NO_SOLUTION"
