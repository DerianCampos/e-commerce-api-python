from datetime import datetime
from typing import Optional

from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.domain.value_objects.role import Role
from src.shared.domain.entities.base_entity import BaseEntity
from src.shared.domain.value_objects.entity_id import EntityId
from src.shared.utils.date_util import get_current_datetime


class UserEntity(BaseEntity):
    """
    User aggregate root.

    Encapsulates all business rules and invariants for user management.
    All state changes must go through domain methods to ensure invariants are maintained.
    """

    def __init__(
        self,
        id: EntityId,
        email: Email,
        first_name: str,
        last_name: str,
        hashed_password: HashedPassword,
        role: Role,
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):

        # Private fields - enforce encapsulation
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._hashed_password = hashed_password
        self._role = role
        self._is_active = is_active

        super().__init__(id, created_at, updated_at)

    # ========== Property Getters (Read-only access) ==========

    @property
    def email(self) -> Email:
        """Get the user's email address."""
        return self._email

    @property
    def first_name(self) -> str:
        """Get the user's first name."""
        return self._first_name

    @property
    def last_name(self) -> str:
        """Get the user's last name."""
        return self._last_name

    @property
    def hashed_password(self) -> HashedPassword:
        """Get the user's hashed password."""
        return self._hashed_password

    @property
    def role(self) -> Role:
        """Get the user's role."""
        return self._role

    @property
    def is_active(self) -> bool:
        """Check if the user account is active."""
        return self._is_active

    # ========== Domain Methods (State changes with invariant enforcement) ==========

    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[Email] = None
    ) -> None:
        """
        Update user profile information atomically (email, first name, and/or last name).

        This method handles partial updates (PATCH semantics) - only non-None fields are updated.
        All changes are applied together with a single updated_at timestamp.

        Args:
            first_name: New first name (if provided)
            last_name: New last name (if provided)
            email: New email address (if provided, already validated as Email value object)

        Raises:
            ValueError: If provided names are invalid (empty, whitespace only, too long)
                       or if email is None (use a valid Email value object)
        """
        changed = False

        if email is not None:
            self._email = email
            changed = True

        if first_name is not None:
            self._first_name = first_name
            changed = True

        if last_name is not None:
            self._last_name = last_name
            changed = True

        # Only update timestamp if at least one field was changed
        if changed:
            self._touch()

    # ========== Private Helper Methods ==========

    def _touch(self) -> None:
        """
        Update the updated_at timestamp to current time.
        Called internally by all state-changing methods.
        """
        self.updated_at = get_current_datetime()

