from uuid import UUID

from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import TShirtSizeResponse
from src.app.features.t_shirt_size.application.mappers.t_shirt_size_mapper import to_t_shirt_size_response
from src.app.features.t_shirt_size.domain.exceptions.t_shirt_size_exception import TShirtSizeDoesNotExistException
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetTShirtSizeByIdUseCase:
    def __init__(self, size_repository: TShirtSizeRepository):
        self.size_repository = size_repository

    async def execute(self, size_id: str) -> TShirtSizeResponse:
        try:
            size_uuid = UUID(size_id)
            size_obj_id = EntityId(size_uuid)

            existing_size = await self.size_repository.find_by_id(size_uuid)

            if not existing_size:
                log.warning(f"T-shirt size not found with ID: {size_id}")
                raise TShirtSizeDoesNotExistException(size_obj_id)

            return to_t_shirt_size_response(existing_size)

        except ValueError as e:
            log.error(f"Invalid UUID format for size ID {size_id}: {e}")
            raise ValueError(f"Invalid size ID format: {size_id}")
        except TShirtSizeDoesNotExistException:
            log.error(f"T-shirt size does not exist with ID: {size_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get t-shirt size by ID for {size_id}: {str(e)}")
            raise
