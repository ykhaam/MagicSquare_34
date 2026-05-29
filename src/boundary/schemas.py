"""Boundary response schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."


class ErrorDetail(BaseModel):
    """Error code and fixed message for a validation failure."""

    code: str
    message: str


class FailureResponse(BaseModel):
    """Failure envelope returned when input validation rejects a grid."""

    type: Literal["ERROR"] = "ERROR"
    error: ErrorDetail
