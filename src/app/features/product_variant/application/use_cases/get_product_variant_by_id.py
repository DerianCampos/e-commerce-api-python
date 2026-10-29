from uuid import UUID

from src.app.features.product_variant.application.dtos.product_variant_dto import ProductVariantResponse
from src.app.features.product_variant.application.mappers.product_variant_mapper import to_product_variant_response
from src.app.features.product_variant.domain.exceptions.product_variant_exception import (
    ProductVariantDoesNotExistException,
)
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetProductVariantByIdUseCase:
    def __init__(self, variant_repository: ProductVariantRepository):
        self.variant_repository = variant_repository

    async def execute(self, variant_id: str) -> ProductVariantResponse:
        try:
            variant_uuid = UUID(variant_id)
            variant_obj_id = EntityId(variant_uuid)

            existing_variant = await self.variant_repository.find_by_id(variant_uuid)

            if not existing_variant:
                log.warning(f"Product variant not found with ID: {variant_id}")
                raise ProductVariantDoesNotExistException(variant_obj_id)

            return to_product_variant_response(existing_variant)

        except ValueError as e:
            log.error(f"Invalid UUID format for variant ID {variant_id}: {e}")
            raise ValueError(f"Invalid variant ID format: {variant_id}")
        except ProductVariantDoesNotExistException:
            log.error(f"Product variant does not exist with ID: {variant_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get product variant by ID for {variant_id}: {str(e)}")
            raise
