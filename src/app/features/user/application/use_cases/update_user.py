from uuid import UUID

from src.app.features.user.application.dtos.user_dto import UserResponse, UserUpdateRequest
from src.app.features.user.application.mappers.user_mapper import to_user_response
from src.app.features.user.domain.exceptions.user_exception import UserDoesNotExistException
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.domain.value_objects.email import Email
from app.shared.domain.value_objects.entity_id import EntityId
from app.shared.utils.log_util import log


class UpdateUserUseCase:
    """
    Use case for partially updating a user's information.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str, user_update: UserUpdateRequest) -> UserResponse:

        try:
            user_uuid = UUID(user_id)
            user_entity_id = EntityId(user_uuid)

            # Fetch existing user
            existing_user = await self.user_repository.find_by_id(user_uuid)

            if not existing_user:
                log.warning(f"Cannot update user. User not found with ID: {user_id}")
                raise UserDoesNotExistException(user_entity_id)

            # Apply partial updates (only non-None fields)
            if user_update.email is not None:
                existing_user.email = Email(user_update.email)

            if user_update.first_name is not None:
                existing_user.first_name = user_update.first_name

            if user_update.last_name is not None:
                existing_user.last_name = user_update.last_name

            # Persist changes
            updated_user = await self.user_repository.update(existing_user)

            log.info(f"User with ID {user_id} successfully updated.")

            return to_user_response(updated_user)

        except ValueError as e:
            log.error(f"Invalid UUID format for user ID {user_id}: {e}")
            raise ValueError(f"Invalid user ID format: {user_id}")
        except UserDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update user for {user_id}: {str(e)}")
            raise

