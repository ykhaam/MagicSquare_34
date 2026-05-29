"""Boundary layer — input validation and UI-facing response envelopes."""

from boundary.input_validator import InputValidator
from boundary.magic_square_boundary import MagicSquareBoundary
from boundary.schemas import ErrorDetail, ErrorResponse, FailureResponse

__all__ = [
    "ErrorDetail",
    "ErrorResponse",
    "FailureResponse",
    "InputValidator",
    "MagicSquareBoundary",
]
