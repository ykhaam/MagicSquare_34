"""Entity tests for User (domain invariants)."""

from __future__ import annotations

import pytest

from entity.exceptions import UserValidationError
from entity.user import User
from entity.user_constants import MAX_DISPLAY_NAME_LENGTH


class TestUserCreate:
    """User creation and factory validation."""

    def test_user_n01_create_valid(self) -> None:
        """Valid id, name, and email produce a User."""
        # Arrange
        user_id = "usr-001"
        display_name = "Learner One"
        email = "learner@example.com"

        # Act
        user = User.create(user_id=user_id, display_name=display_name, email=email)

        # Assert
        assert user.user_id == user_id
        assert user.display_name == display_name
        assert user.email == email

    def test_user_e01_empty_user_id(self) -> None:
        """Empty user_id is rejected."""
        # Arrange
        user_id = ""
        display_name = "Learner"
        email = "a@b.co"

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(user_id=user_id, display_name=display_name, email=email)

        assert exc_info.value.code == "USER_INVALID_ID"

    def test_user_e02_display_name_too_short(self) -> None:
        """Display name shorter than minimum is rejected."""
        # Arrange
        too_short = ""

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(
                user_id="usr-002",
                display_name=too_short,
                email="a@b.co",
            )

        assert exc_info.value.code == "USER_INVALID_DISPLAY_NAME"

    def test_user_e03_display_name_too_long(self) -> None:
        """Display name longer than maximum is rejected."""
        # Arrange
        too_long = "x" * (MAX_DISPLAY_NAME_LENGTH + 1)

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(
                user_id="usr-003",
                display_name=too_long,
                email="a@b.co",
            )

        assert exc_info.value.code == "USER_INVALID_DISPLAY_NAME"

    def test_user_e04_invalid_email(self) -> None:
        """Malformed email is rejected."""
        # Arrange
        email = "not-an-email"

        # Act / Assert
        with pytest.raises(UserValidationError) as exc_info:
            User.create(
                user_id="usr-004",
                display_name="Learner",
                email=email,
            )

        assert exc_info.value.code == "USER_INVALID_EMAIL"


class TestUserBehavior:
    """User identity and mutation rules."""

    def test_user_n02_rename_display_name(self) -> None:
        """rename returns a new User with updated display name."""
        # Arrange
        user = User.create(
            user_id="usr-005",
            display_name="Before",
            email="before@example.com",
        )
        new_name = "After"

        # Act
        updated = user.rename_display_name(new_name)

        # Assert
        assert updated.display_name == new_name
        assert updated.user_id == user.user_id
        assert updated.email == user.email
        assert user.display_name == "Before"

    def test_user_n03_same_identity_by_user_id(self) -> None:
        """Users with the same user_id are considered the same identity."""
        # Arrange
        left = User.create("usr-006", "A", "a@example.com")
        right = User.create("usr-006", "B", "b@example.com")

        # Act
        same = left.is_same_identity_as(right)

        # Assert
        assert same is True

    def test_user_n04_different_identity(self) -> None:
        """Different user_id means different identity."""
        # Arrange
        left = User.create("usr-007", "A", "a@example.com")
        right = User.create("usr-008", "A", "a@example.com")

        # Act
        same = left.is_same_identity_as(right)

        # Assert
        assert same is False
