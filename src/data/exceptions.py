"""Data-layer exceptions."""

from __future__ import annotations

from entity.domain_codes import (
    DATA_CORRUPT_CODE,
    DATA_CORRUPT_MESSAGE,
    DATA_INVALID_GRID_CODE,
    DATA_INVALID_GRID_MESSAGE,
    DATA_INVALID_ID_CODE,
    DATA_INVALID_ID_MESSAGE,
    DATA_INVALID_RESULT_CODE,
    DATA_INVALID_RESULT_MESSAGE,
    DATA_NOT_FOUND_CODE,
    DATA_NOT_FOUND_MESSAGE,
)


class DataError(Exception):
    """Base data-layer error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        """Initialize with code and message."""
        super().__init__(message)
        self.code = code
        self.message = message


class DataNotFoundError(DataError):
    """Raised when a stored id does not exist."""

    def __init__(
        self,
        code: str = DATA_NOT_FOUND_CODE,
        message: str = DATA_NOT_FOUND_MESSAGE,
    ) -> None:
        """Initialize with DATA_NOT_FOUND defaults."""
        super().__init__(code, message)


class DataInvalidGridError(DataError):
    """Raised when a grid fails persistence validation."""

    def __init__(
        self,
        code: str = DATA_INVALID_GRID_CODE,
        message: str = DATA_INVALID_GRID_MESSAGE,
    ) -> None:
        """Initialize with DATA_INVALID_GRID defaults."""
        super().__init__(code, message)


class DataInvalidIdError(DataError):
    """Raised when a storage id is blank."""

    def __init__(
        self,
        code: str = DATA_INVALID_ID_CODE,
        message: str = DATA_INVALID_ID_MESSAGE,
    ) -> None:
        """Initialize with DATA_INVALID_ID defaults."""
        super().__init__(code, message)


class DataInvalidResultError(DataError):
    """Raised when a stored result vector is invalid."""

    def __init__(
        self,
        code: str = DATA_INVALID_RESULT_CODE,
        message: str = DATA_INVALID_RESULT_MESSAGE,
    ) -> None:
        """Initialize with DATA_INVALID_RESULT defaults."""
        super().__init__(code, message)


class DataCorruptError(DataError):
    """Raised when stored bytes cannot be parsed."""

    def __init__(
        self,
        code: str = DATA_CORRUPT_CODE,
        message: str = DATA_CORRUPT_MESSAGE,
    ) -> None:
        """Initialize with DATA_CORRUPT defaults."""
        super().__init__(code, message)
