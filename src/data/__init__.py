"""Data layer — persistence adapters."""

from data.exceptions import (
    DataCorruptError,
    DataError,
    DataInvalidGridError,
    DataInvalidIdError,
    DataInvalidResultError,
    DataNotFoundError,
)
from data.matrix_repository import InMemoryMatrixRepository, InMemoryResultRepository

__all__ = [
    "DataCorruptError",
    "DataError",
    "DataInvalidGridError",
    "DataInvalidIdError",
    "DataInvalidResultError",
    "DataNotFoundError",
    "InMemoryMatrixRepository",
    "InMemoryResultRepository",
]
