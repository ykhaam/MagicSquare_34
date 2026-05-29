"""Boundary entrypoint for magic-square solve requests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from boundary.input_validator import InputValidator
from boundary.schemas import ErrorResponse, FailureResponse
from entity.exceptions import UnsolvableDomainError


class MagicSquareBoundary:
    """Validates input and delegates valid grids to the injected resolve callable."""

    def __init__(self, resolve: Callable[..., Any]) -> None:
        """Wire Domain resolve; validation failures never invoke resolve.

        Args:
            resolve: Stand-in or real Domain entrypoint for valid grids.
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
            return self._resolve(grid)
        except UnsolvableDomainError as exc:
            return ErrorResponse(code=exc.code, message=exc.message)


class UIBoundary(MagicSquareBoundary):
    """UI-facing boundary alias that injects Control ``execute`` instead of resolve."""

    def __init__(self, execute: Callable[..., Any]) -> None:
        """Wire Control execute callable.

        Args:
            execute: Control-layer puzzle solver entrypoint.
        """
        super().__init__(resolve=execute)
