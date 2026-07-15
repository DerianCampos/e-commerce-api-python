from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.features.user.domain.value_objects.role import Role
from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword

class UserModelMapper:

    @staticmethod
    def to_user_model(user_entity):
        return {
            "id": str(user_entity.id.value),
            "email": user_entity.email.value,
            "first_name": user_entity.first_name,
            "last_name": user_entity.last_name,
            "role": user_entity.role.value,
            "is_active": user_entity.is_active,
            "created_at": user_entity.created_at,
            "updated_at": user_entity.updated_at,
        }
    
    @staticmethod
    def to_user_entity(user_model):
        if user_model is None:
            return None
        return UserEntity(
            id=EntityId(user_model.id),
            email=Email(user_model.email),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            password=HashedPassword(user_model.password),
            role=Role.from_str(user_model.role),
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )