from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.infrastructure.postgres.models.user_model import UserModel
from src.shared.domain.value_objects.entity_id import EntityId
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.domain.value_objects.role import Role


def map_model_to_entity(user_model: UserModel):
    """Maps a user model to a user entity, wrapping primitives into domain value objects."""

    if user_model is None:
        return None

    return UserEntity(
        id=EntityId(user_model.id),
        email=Email(user_model.email),
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        hashed_password=HashedPassword(user_model.hashed_password),
        role=Role.from_str(user_model.role),
        is_active=bool(user_model.is_active),
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
    )
