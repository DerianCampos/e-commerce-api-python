from uuid import UUID

from src.app.features.product_variant.domain.exceptions.product_variant_exception import (
    ProductVariantDoesNotExistException,
)
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteProductVariantUseCase:
    def __init__(self, variant_repository: ProductVariantRepository):
        self.variant_repository = variant_repository

    async def execute(self, variant_id: str) -> bool:

        try:
            variant_uuid = UUID(variant_id)
            variant_entity_id = EntityId(variant_uuid)

            variant_exists = await self.variant_repository.exists(variant_uuid)

            if not variant_exists:
                log.warning(f"Cannot delete product variant. Variant not found with ID: {variant_id}")
                raise ProductVariantDoesNotExistException(variant_entity_id)

            deleted = await self.variant_repository.delete(variant_uuid)

            if deleted:
                log.info(f"Product variant with ID {variant_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for variant ID {variant_id}: {e}")
            raise ValueError(f"Invalid variant ID format: {variant_id}")
        except ProductVariantDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete product variant for {variant_id}: {str(e)}")
            raise
