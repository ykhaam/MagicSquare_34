"""Boundary response_contract guard branches."""

from __future__ import annotations

from boundary.error_codes import UI_INTERNAL_CONTRACT_CODE
from boundary.response_contract import map_domain_exception, validate_success_vector
from entity.exceptions import DomainInvalidGridError, UnsolvableDomainError


class TestResponseContract:
    """UT-F01/F02 helpers and domain exception mapping."""

    def test_map_domain_exception_returns_none_for_unknown(self) -> None:
        """Unknown exceptions are not mapped at Boundary."""
        assert map_domain_exception(ValueError("x")) is None

    def test_validate_non_list_returns_internal_contract(self) -> None:
        """Non-list resolve results violate int[6] contract."""
        result = validate_success_vector("not-a-list")

        assert result is not None
        assert result.code == UI_INTERNAL_CONTRACT_CODE

    def test_map_unsolvable_domain_error(self) -> None:
        """UnsolvableDomainError maps to flat ErrorResponse."""
        mapped = map_domain_exception(UnsolvableDomainError())

        assert mapped is not None
        assert mapped.code == "DOMAIN_NO_SOLUTION"

    def test_map_domain_invalid_grid_error(self) -> None:
        """DomainInvalidGridError maps to flat ErrorResponse."""
        mapped = map_domain_exception(DomainInvalidGridError())

        assert mapped is not None
        assert mapped.code == "DOMAIN_INVALID_GRID"
