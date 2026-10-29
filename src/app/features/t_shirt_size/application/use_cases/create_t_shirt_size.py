from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import TShirtSizeCreateRequest, TShirtSizeResponse
from src.app.features.t_shirt_size.application.mappers.t_shirt_size_mapper import (
    to_t_shirt_size_entity,
    to_t_shirt_size_response,
)
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.utils.log_util import log


class CreateTShirtSizeUseCase:
    def __init__(self, size_repository: TShirtSizeRepository):
        self.size_repository = size_repository

    async def execute(self, payload: TShirtSizeCreateRequest) -> TShirtSizeResponse:
        try:
            size_entity = to_t_shirt_size_entity(payload)

            created_size = await self.size_repository.save(size_entity)
            log.info(f"T-shirt size created: {created_size.size}")

            return to_t_shirt_size_response(created_size)

        except Exception as e:
            log.error(f"Unexpected error while saving t-shirt size: {str(e)}")
            raise
