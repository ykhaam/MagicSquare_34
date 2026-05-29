"""Domain-level exceptions for entity layer."""

from __future__ import annotations

from entity.domain_codes import (
    DOMAIN_INVALID_GRID_CODE,
    DOMAIN_INVALID_GRID_MESSAGE,
)

DOMAIN_NO_SOLUTION_CODE = "DOMAIN_NO_SOLUTION"
DOMAIN_NO_SOLUTION_MESSAGE = (
    "No valid magic square completion for the two empty cells."
)


class UserValidationError(ValueError):
    """Raised when User invariants are violated.

    Attributes:
        code: Machine-readable error code for mapping at boundary layer.
    """

    def __init__(self, code: str, message: str) -> None:
        """Initialize with a stable error code and human-readable message.

        Args:
            code: Domain error identifier (e.g. USER_INVALID_EMAIL).
            message: Description of the validation failure.
        """
        super().__init__(message)
        self.code = code


class UnsolvableDomainError(Exception):
    """Raised when no valid magic-square completion exists for the puzzle."""

    def __init__(
        self,
        code: str = DOMAIN_NO_SOLUTION_CODE,
        message: str = DOMAIN_NO_SOLUTION_MESSAGE,
    ) -> None:
        """Initialize with domain no-solution contract fields.

        Args:
            code: Fixed domain error code.
            message: Fixed domain error message.
        """
        super().__init__(message)
        self.code = code
        self.message = message


class DomainInvalidGridError(Exception):
    """Raised when a grid fails domain structure validation."""

    def __init__(
        self,
        code: str = DOMAIN_INVALID_GRID_CODE,
        message: str = DOMAIN_INVALID_GRID_MESSAGE,
    ) -> None:
        """Initialize with domain invalid-grid contract fields."""
        super().__init__(message)
        self.code = code
        self.message = message
