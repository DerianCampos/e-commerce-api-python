from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.application.dtos.user_dto_mapper import map_entity_to_dto_user
from src.app.features.user.application.dtos.user_dto import UserCreate, UserResponse
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.role import Role
from src.shared.domain.value_objects.entity_id import EntityId
from src.shared.utils.log_util import log

class SaveUser:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_create: UserCreate) -> UserResponse:
        try:
            # Build the domain entity from the incoming DTO
            entity_id = EntityId.generate()
            email_vo = Email(user_create.email)
            role_vo = Role.from_str(user_create.role)

            user_entity = UserEntity(
                id=entity_id,
                email=email_vo,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                role=role_vo,
                is_active=True,
            )

            saved_user = await self.user_repository.save(user_entity)
            log.info(saved_user.first_name)
            response_dto = map_entity_to_dto_user(saved_user)

            return response_dto

        except Exception as e:
            log.error(f"Unexpected error while saving user: {str(e)}")
            raise