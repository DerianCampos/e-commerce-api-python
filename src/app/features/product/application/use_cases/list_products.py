from typing import List, Optional

from src.app.features.product.application.dtos.product_dto import ProductResponse
from src.app.features.product.application.mappers.product_mapper import to_product_response
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.shared.utils.log_util import log


class ListProductsUseCase:
    """
    Use case for listing all products with optional pagination.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ProductResponse]:
        try:
            products = await self.product_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(products)} products.")

            return [to_product_response(product) for product in products]

        except Exception as e:
            log.error(f"Unexpected error during list products: {str(e)}")
            raise
