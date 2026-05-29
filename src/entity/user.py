"""User entity — domain identity for MagicSquare learners."""

from __future__ import annotations

import re
from dataclasses import dataclass

from entity.exceptions import UserValidationError
from entity.user_constants import (
    ERROR_USER_INVALID_DISPLAY_NAME,
    ERROR_USER_INVALID_EMAIL,
    ERROR_USER_INVALID_ID,
    MAX_DISPLAY_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_USER_ID_LENGTH,
    MIN_DISPLAY_NAME_LENGTH,
)

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class User:
    """Immutable domain entity representing a puzzle learner.

    Attributes:
        user_id: Stable unique identifier (non-empty, bounded length).
        display_name: Human-readable name shown in the UI.
        email: Contact email used for identification notifications.
    """

    user_id: str
    display_name: str
    email: str

    @classmethod
    def create(cls, user_id: str, display_name: str, email: str) -> User:
        """Create a User after validating all invariants.

        Args:
            user_id: Unique identifier for the learner.
            display_name: Display name for UI presentation.
            email: Valid email address string.

        Returns:
            A validated User instance.

        Raises:
            UserValidationError: If any invariant is violated.
        """
        cls._validate_user_id(user_id)
        cls._validate_display_name(display_name)
        cls._validate_email(email)
        return cls(user_id=user_id.strip(), display_name=display_name.strip(), email=email.strip())

    def rename_display_name(self, new_name: str) -> User:
        """Return a new User with an updated display name.

        Args:
            new_name: Replacement display name.

        Returns:
            New User instance; ``user_id`` and ``email`` are unchanged.

        Raises:
            UserValidationError: If ``new_name`` fails display name rules.
        """
        self._validate_display_name(new_name)
        return User(
            user_id=self.user_id,
            display_name=new_name.strip(),
            email=self.email,
        )

    def is_same_identity_as(self, other: User) -> bool:
        """Check whether two users represent the same identity.

        Args:
            other: Another User to compare.

        Returns:
            True if both share the same ``user_id``.
        """
        return self.user_id == other.user_id

    @staticmethod
    def _validate_user_id(user_id: str) -> None:
        """Validate user_id invariant.

        Args:
            user_id: Candidate identifier.

        Raises:
            UserValidationError: If user_id is empty or too long.
        """
        normalized = user_id.strip()
        if not normalized or len(normalized) > MAX_USER_ID_LENGTH:
            raise UserValidationError(
                ERROR_USER_INVALID_ID,
                "user_id must be non-empty and within max length.",
            )

    @staticmethod
    def _validate_display_name(display_name: str) -> None:
        """Validate display_name invariant.

        Args:
            display_name: Candidate display name.

        Raises:
            UserValidationError: If length rules are violated.
        """
        normalized = display_name.strip()
        if (
            len(normalized) < MIN_DISPLAY_NAME_LENGTH
            or len(normalized) > MAX_DISPLAY_NAME_LENGTH
        ):
            raise UserValidationError(
                ERROR_USER_INVALID_DISPLAY_NAME,
                "display_name length is out of allowed range.",
            )

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email invariant.

        Args:
            email: Candidate email address.

        Raises:
            UserValidationError: If format or length is invalid.
        """
        normalized = email.strip()
        if len(normalized) > MAX_EMAIL_LENGTH or not _EMAIL_PATTERN.match(normalized):
            raise UserValidationError(
                ERROR_USER_INVALID_EMAIL,
                "email must be a valid address within max length.",
            )
