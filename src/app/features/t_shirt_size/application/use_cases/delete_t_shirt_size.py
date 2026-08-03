from uuid import UUID

from src.app.features.t_shirt_size.domain.exceptions.t_shirt_size_exception import TShirtSizeDoesNotExistException
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteTShirtSizeUseCase:
    def __init__(self, size_repository: TShirtSizeRepository):
        self.size_repository = size_repository

    async def execute(self, size_id: str) -> bool:

        try:
            size_uuid = UUID(size_id)
            size_entity_id = EntityId(size_uuid)

            size_exists = await self.size_repository.exists(size_uuid)

            if not size_exists:
                log.warning(f"Cannot delete t-shirt size. Size not found with ID: {size_id}")
                raise TShirtSizeDoesNotExistException(size_entity_id)

            deleted = await self.size_repository.delete(size_uuid)

            if deleted:
                log.info(f"T-shirt size with ID {size_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for size ID {size_id}: {e}")
            raise ValueError(f"Invalid size ID format: {size_id}")
        except TShirtSizeDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete t-shirt size for {size_id}: {str(e)}")
            raise
