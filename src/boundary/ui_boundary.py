"""Boundary SSOT — validation, solve delegation, and UI-facing entrypoint."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from boundary.input_validator import InputValidator
from boundary.response_contract import map_domain_exception, validate_success_vector
from boundary.schemas import ErrorResponse


class MagicSquareBoundary:
    """Validates input and delegates valid grids to the injected resolve callable."""

    def __init__(self, resolve: Callable[..., Any]) -> None:
        """Wire resolve; validation failures never invoke resolve.

        Args:
            resolve: Control or test double entrypoint for valid grids.
        """
        self._resolve = resolve
        self._validator = InputValidator()

    def solve(self, grid: list[list[int]] | None) -> ErrorResponse | list[int]:
        """Validate grid; return ErrorResponse or delegate to resolve on success.

        Args:
            grid: 4×4 puzzle grid, or None when absent.

        Returns:
            ErrorResponse on validation failure, otherwise resolve result.
        """
        failure = self._validator.validate(grid)
        if failure is not None:
            return ErrorResponse(
                code=failure.error.code,
                message=failure.error.message,
            )
        try:
            raw_result = self._resolve(grid)
        except Exception as exc:
            mapped = map_domain_exception(exc)
            if mapped is not None:
                return mapped
            raise

        contract_error = validate_success_vector(raw_result)
        if contract_error is not None:
            return contract_error
        return raw_result


class UIBoundary(MagicSquareBoundary):
    """UI-facing boundary that injects Control ``execute`` instead of resolve."""

    def __init__(self, execute: Callable[..., Any]) -> None:
        """Wire Control execute callable.

        Args:
            execute: Control-layer puzzle solver entrypoint.
        """
        super().__init__(resolve=execute)


__all__ = ["MagicSquareBoundary", "UIBoundary"]
