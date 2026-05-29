"""Domain-level exceptions for entity layer."""


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
