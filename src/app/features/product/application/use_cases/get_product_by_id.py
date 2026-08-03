from uuid import UUID

from src.app.features.product.application.dtos.product_dto import ProductResponse
from src.app.features.product.application.mappers.product_mapper import to_product_response
from src.app.features.product.domain.exceptions.product_exception import ProductDoesNotExistException
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetProductByIdUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: str) -> ProductResponse:
        try:
            product_uuid = UUID(product_id)

            existing_product = await self.product_repository.find_by_id(product_uuid)

            if not existing_product:
                log.warning(f"Product not found with ID: {product_id}")
                raise ProductDoesNotExistException(EntityId(product_uuid))

            response_dto = to_product_response(existing_product)

            return response_dto

        except ValueError as e:
            log.error(f"Invalid UUID format for product ID {product_id}: {e}")
            raise ValueError(f"Invalid product ID format: {product_id}")
        except ProductDoesNotExistException:
            log.error(f"Product does not exist with ID: {product_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get product by ID for {product_id}: {str(e)}")
            raise
