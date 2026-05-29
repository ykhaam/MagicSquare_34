"""Domain error codes and messages (Report 02 §2.4)."""

from __future__ import annotations

from typing import Final

DOMAIN_INVALID_GRID_CODE: Final[str] = "DOMAIN_INVALID_GRID"
DOMAIN_INVALID_GRID_MESSAGE: Final[str] = "Grid failed domain validation."

DATA_NOT_FOUND_CODE: Final[str] = "DATA_NOT_FOUND"
DATA_NOT_FOUND_MESSAGE: Final[str] = "Stored grid was not found."

DATA_INVALID_GRID_CODE: Final[str] = "DATA_INVALID_GRID"
DATA_INVALID_GRID_MESSAGE: Final[str] = "Stored grid failed validation."

DATA_INVALID_ID_CODE: Final[str] = "DATA_INVALID_ID"
DATA_INVALID_ID_MESSAGE: Final[str] = "Storage id must be a non-empty string."

DATA_INVALID_RESULT_CODE: Final[str] = "DATA_INVALID_RESULT"
DATA_INVALID_RESULT_MESSAGE: Final[str] = "Stored result must be a six-element vector."

DATA_CORRUPT_CODE: Final[str] = "DATA_CORRUPT"
DATA_CORRUPT_MESSAGE: Final[str] = "Stored data is corrupt."
