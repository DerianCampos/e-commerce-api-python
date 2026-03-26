from typing import Union

from pydantic import BaseModel

from src.app.features.user.application.dtos.user_dto import UserResponse
from src.app.features.user.domain.entities.user_entity import UserEntity


def map_entity_to_dto_user(user_entity:  Union[BaseModel, UserEntity]) -> UserResponse:
    """
    Convert a User Entity to a User DTO (Data Transfer Object).
    """

    full_name = f"{user_entity.first_name} {user_entity.last_name}"
    return UserResponse(
        id=str(user_entity.id.value),
        email=str(user_entity.email.value),
        full_name=full_name,
        role=str(user_entity.role.value),
        is_active=bool(user_entity.is_active),
    )
