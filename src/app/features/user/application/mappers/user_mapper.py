from typing import Union

from pydantic import BaseModel

from app.shared.domain.value_objects.entity_id import EntityId
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.role import Role
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.application.dtos.user_dto import UserResponse
from src.app.features.user.domain.entities.user_entity import UserEntity


def to_user_response(user_entity:  Union[BaseModel, UserEntity]) -> UserResponse:
    """
    Convert a User Entity to a User DTO (Data Transfer Object).
    """
    return UserResponse(
        id=str(user_entity.id.value),
        first_name=user_entity.first_name,
        last_name=user_entity.last_name,
        email=str(user_entity.email.value),
        role=str(user_entity.role.value),
        is_active=bool(user_entity.is_active),
    )

def to_user_entity(user_dto: UserResponse) -> UserEntity:
    """
    Convert a User DTO (Data Transfer Object) to a User Entity.
    """
    return UserEntity.create(
        id=EntityId.generate(),
        first_name=user_dto.first_name,
        last_name=user_dto.last_name,
        email=Email(user_dto.email),
        role=Role.from_str(user_dto.role),
        is_active=user_dto.is_active,
        hashed_password=HashedPassword.from_plain_text(user_dto.hashed_password)
    )
