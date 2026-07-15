from uuid import UUID

from src.app.features.user.domain.exceptions.user_exception import UserDoesNotExistException
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteUserUseCase:
    """
    Use case for deleting a user by their ID.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> bool:

        try:
            user_uuid = UUID(user_id)
            user_entity_id = EntityId(user_uuid)

            # Check if user exists before attempting deletion
            user_exists = await self.user_repository.exists(user_uuid)

            if not user_exists:
                log.warning(f"Cannot delete user. User not found with ID: {user_id}")
                raise UserDoesNotExistException(user_entity_id)

            # Perform deletion
            deleted = await self.user_repository.delete(user_uuid)

            if deleted:
                log.info(f"User with ID {user_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for user ID {user_id}: {e}")
            raise ValueError(f"Invalid user ID format: {user_id}")
        except UserDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete user for {user_id}: {str(e)}")
            raise

