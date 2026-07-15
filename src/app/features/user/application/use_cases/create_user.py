from src.app.features.user.application.dtos.user_dto import UserCreateRequest, UserResponse
from src.app.features.user.application.mappers.user_mapper import to_user_response, to_user_entity
from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.hashed_password import HashedPassword
from src.app.features.user.domain.value_objects.role import Role
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class CreateUserUseCase:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, payload: UserCreateRequest) -> UserResponse:
        try:

            user_entity = to_user_entity(payload)

            created_user = await self.user_repository.save(user_entity)
            log.info(created_user.first_name)
            response_dto = to_user_response(created_user)

            return response_dto

        except Exception as e:
            log.error(f"Unexpected error while saving user: {str(e)}")
            raise
