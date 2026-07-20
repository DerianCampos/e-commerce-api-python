from typing import List, Optional

from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import TShirtSizeResponse
from src.app.features.t_shirt_size.application.mappers.t_shirt_size_mapper import to_t_shirt_size_response
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.utils.log_util import log


class ListTShirtSizesUseCase:
    def __init__(self, size_repository: TShirtSizeRepository):
        self.size_repository = size_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[TShirtSizeResponse]:
        try:
            sizes = await self.size_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(sizes)} t-shirt sizes.")

            return [to_t_shirt_size_response(size) for size in sizes]

        except Exception as e:
            log.error(f"Unexpected error during list t-shirt sizes: {str(e)}")
            raise
