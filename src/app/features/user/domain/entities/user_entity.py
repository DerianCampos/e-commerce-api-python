from datetime import datetime
from typing import Optional

from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.domain.value_objects.role import Role
from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class UserEntity(BaseEntity):

    def __init__(
        self,
        id: EntityId,
        email: Email,
        first_name: str,
        last_name: str,
        password: HashedPassword,
        role: Role,
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._role = role
        self._is_active = is_active
        super().__init__(id, created_at, updated_at)

    @property
    def email(self) -> Email:
        return self._email

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def role(self) -> Role:
        return self._role

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def password(self) -> HashedPassword:
        return self._password

    @classmethod
    def create(
        cls,
        email: Email,
        first_name: str,
        last_name: str,
        password: HashedPassword,
        role: Role,
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> "UserEntity":
        return cls(
            id=EntityId.generate(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def update(
        self,
        email: Optional[Email] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[HashedPassword] = None,
        role: Optional[Role] = None,
        is_active: Optional[bool] = None
    ) -> None:
        if email is not None:
            self._email = email
        if first_name is not None:
            self._first_name = first_name
        if last_name is not None:
            self._last_name = last_name
        if password is not None:
            self._password = password
        if role is not None:
            self._role = role
        if is_active is not None:
            self._is_active = is_active
        self.mark_as_updated()
