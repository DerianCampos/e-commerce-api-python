from typing import Optional
from uuid import UUID

from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import TShirtSizeResponse, TShirtSizeUpdateRequest
from src.app.features.t_shirt_size.application.mappers.t_shirt_size_mapper import to_t_shirt_size_response
from src.app.features.t_shirt_size.domain.exceptions.t_shirt_size_exception import TShirtSizeDoesNotExistException
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.features.t_shirt_size.domain.value_objects.size import Size
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateTShirtSizeUseCase:
    def __init__(self, size_repository: TShirtSizeRepository):
        self.size_repository = size_repository

    async def execute(self, size_id: str, size_update: TShirtSizeUpdateRequest) -> TShirtSizeResponse:

        try:
            size_uuid = UUID(size_id)
            size_entity_id = EntityId(size_uuid)

            existing_size = await self.size_repository.find_by_id(size_uuid)

            if not existing_size:
                log.warning(f"Cannot update t-shirt size. Size not found with ID: {size_id}")
                raise TShirtSizeDoesNotExistException(size_entity_id)

            size: Optional[Size] = None
            if size_update.size is not None:
                size = Size.from_str(size_update.size)

            existing_size.update(
                size=size,
                chest_min_cm=size_update.chest_min_cm,
                chest_max_cm=size_update.chest_max_cm,
            )

            updated_size = await self.size_repository.update(existing_size)

            log.info(f"T-shirt size with ID {size_id} successfully updated.")

            return to_t_shirt_size_response(updated_size)

        except ValueError as e:
            log.error(f"Invalid UUID format for size ID {size_id}: {e}")
            raise ValueError(f"Invalid size ID format: {size_id}")
        except TShirtSizeDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update t-shirt size for {size_id}: {str(e)}")
            raise
