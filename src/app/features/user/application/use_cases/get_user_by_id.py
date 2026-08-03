from uuid import UUID

from src.app.features.user.application.dtos.user_dto import UserResponse
from src.app.features.user.application.mappers.user_mapper import to_user_response
from src.app.features.user.domain.exceptions.user_exception import UserDoesNotExistException
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetUserByIdUseCase:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> UserResponse:
        try:
            user_uuid = UUID(user_id)

            existing_user = await self.user_repository.find_by_id(user_uuid)

            if not existing_user:
                log.warning(f"User not found with ID: {user_id}")
                raise UserDoesNotExistException(EntityId(user_uuid))

            response_dto = to_user_response(existing_user)

            return response_dto

        except ValueError as e:
            log.error(f"Invalid UUID format for user ID {user_id}: {e}")
            raise ValueError(f"Invalid user ID format: {user_id}")
        except UserDoesNotExistException:
            log.error(f"User does not exist with ID: {user_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get user by ID for {user_id}: {str(e)}")
            raise
