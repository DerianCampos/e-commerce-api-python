from src.app.features.product_variant.application.dtos.product_variant_dto import (
    ProductVariantCreateRequest,
    ProductVariantResponse,
)
from src.app.features.product_variant.application.mappers.product_variant_mapper import (
    to_product_variant_entity,
    to_product_variant_response,
)
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.shared.utils.log_util import log


class CreateProductVariantUseCase:
    def __init__(self, variant_repository: ProductVariantRepository):
        self.variant_repository = variant_repository

    async def execute(self, payload: ProductVariantCreateRequest) -> ProductVariantResponse:
        try:
            variant_entity = to_product_variant_entity(payload)

            created_variant = await self.variant_repository.save(variant_entity)
            log.info(f"Product variant created with SKU: {created_variant.sku}")

            return to_product_variant_response(created_variant)

        except Exception as e:
            log.error(f"Unexpected error while saving product variant: {str(e)}")
            raise
