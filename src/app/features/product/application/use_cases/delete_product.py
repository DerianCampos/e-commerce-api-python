from uuid import UUID

from src.app.features.product.domain.exceptions.product_exception import ProductDoesNotExistException
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteProductUseCase:
    """
    Use case for deleting a product by its ID.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: str) -> bool:

        try:
            product_uuid = UUID(product_id)
            product_entity_id = EntityId(product_uuid)

            product_exists = await self.product_repository.exists(product_uuid)

            if not product_exists:
                log.warning(f"Cannot delete product. Product not found with ID: {product_id}")
                raise ProductDoesNotExistException(product_entity_id)

            deleted = await self.product_repository.delete(product_uuid)

            if deleted:
                log.info(f"Product with ID {product_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for product ID {product_id}: {e}")
            raise ValueError(f"Invalid product ID format: {product_id}")
        except ProductDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete product for {product_id}: {str(e)}")
            raise
