"""Boundary layer — input validation and UI-facing response envelopes."""

from boundary.input_validator import InputValidator
from boundary.schemas import ErrorDetail, FailureResponse

__all__ = ["ErrorDetail", "FailureResponse", "InputValidator"]
