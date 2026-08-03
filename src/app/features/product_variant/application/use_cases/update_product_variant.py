from decimal import Decimal
from uuid import UUID

from src.app.features.product_variant.application.dtos.product_variant_dto import (
    ProductVariantResponse,
    ProductVariantUpdateRequest,
)
from src.app.features.product_variant.application.mappers.product_variant_mapper import to_product_variant_response
from src.app.features.product_variant.domain.exceptions.product_variant_exception import (
    ProductVariantDoesNotExistException,
)
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.features.product_variant.domain.value_objects.sku import Sku
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateProductVariantUseCase:
    def __init__(self, variant_repository: ProductVariantRepository):
        self.variant_repository = variant_repository

    async def execute(self, variant_id: str, variant_update: ProductVariantUpdateRequest) -> ProductVariantResponse:

        try:
            variant_uuid = UUID(variant_id)
            variant_entity_id = EntityId(variant_uuid)

            existing_variant = await self.variant_repository.find_by_id(variant_uuid)

            if not existing_variant:
                log.warning(f"Cannot update product variant. Variant not found with ID: {variant_id}")
                raise ProductVariantDoesNotExistException(variant_entity_id)

            existing_variant.update(
                color=variant_update.color,
                sku=Sku(variant_update.sku) if variant_update.sku is not None else None,
                unit_price=Decimal(str(variant_update.unit_price)) if variant_update.unit_price is not None else None,
                stock_quantity=variant_update.stock_quantity,
            )

            updated_variant = await self.variant_repository.update(existing_variant)

            log.info(f"Product variant with ID {variant_id} successfully updated.")

            return to_product_variant_response(updated_variant)

        except ValueError as e:
            log.error(f"Invalid UUID format for variant ID {variant_id}: {e}")
            raise ValueError(f"Invalid variant ID format: {variant_id}")
        except ProductVariantDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update product variant for {variant_id}: {str(e)}")
            raise
