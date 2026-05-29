"""Boundary output guard and domain exception mapping (Report 02 §2.3–2.4)."""

from __future__ import annotations

from typing import Any

from boundary.error_codes import (
    UI_INTERNAL_CONTRACT_CODE,
    UI_INTERNAL_CONTRACT_MESSAGE,
)
from boundary.schemas import ErrorResponse
from entity.constants import (
    GRID_SIZE,
    MAX_CELL_VALUE,
    MIN_CELL_VALUE,
)
from entity.exceptions import DomainInvalidGridError, UnsolvableDomainError

_SUCCESS_VECTOR_LENGTH = 6


def map_domain_exception(exc: Exception) -> ErrorResponse | None:
    """Map domain exceptions to flat Boundary error responses.

    Args:
        exc: Exception raised by the injected resolve callable.

    Returns:
        ErrorResponse when ``exc`` is a known domain failure; otherwise None.
    """
    if isinstance(exc, (DomainInvalidGridError, UnsolvableDomainError)):
        return ErrorResponse(code=exc.code, message=exc.message)
    return None


def validate_success_vector(result: Any) -> ErrorResponse | None:
    """Reject resolve results that violate the public ``int[6]`` contract.

    Args:
        result: Value returned from resolve on success.

    Returns:
        ErrorResponse with ``UI_INTERNAL_CONTRACT`` when validation fails.
    """
    if not isinstance(result, list):
        return _internal_contract_error()
    if len(result) != _SUCCESS_VECTOR_LENGTH:
        return _internal_contract_error()

    r1, c1, n1, r2, c2, n2 = result
    if not all(isinstance(value, int) for value in (r1, c1, n1, r2, c2, n2)):
        return _internal_contract_error()

    for coord in (r1, c1, r2, c2):
        if coord < 1 or coord > GRID_SIZE:
            return _internal_contract_error()

    for fill in (n1, n2):
        if fill < MIN_CELL_VALUE or fill > MAX_CELL_VALUE:
            return _internal_contract_error()

    if n1 == n2:
        return _internal_contract_error()

    return None


def _internal_contract_error() -> ErrorResponse:
    """Build the fixed internal contract violation response."""
    return ErrorResponse(
        code=UI_INTERNAL_CONTRACT_CODE,
        message=UI_INTERNAL_CONTRACT_MESSAGE,
    )
