"""Boundary response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from boundary.error_codes import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE

__all__ = [
    "INVALID_SIZE_CODE",
    "INVALID_SIZE_MESSAGE",
    "ErrorDetail",
    "ErrorResponse",
    "FailureResponse",
]


class ErrorDetail(BaseModel):
    """Error code and fixed message for a validation failure."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Flat error payload returned from Boundary solve on validation failure."""

    code: str
    message: str
    field: str | None = None


class FailureResponse(BaseModel):
    """Failure envelope returned when input validation rejects a grid."""

    type: Literal["ERROR"] = "ERROR"
    error: ErrorDetail
