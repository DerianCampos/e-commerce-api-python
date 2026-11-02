from uuid import UUID

from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.features.product_variant.application.dtos.product_variant_dto import (
    ProductVariantCreateRequest,
    ProductVariantResponse,
)
from src.app.features.product_variant.application.mappers.product_variant_mapper import (
    to_product_variant_entity,
    to_product_variant_response,
)
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.features.product_variant.domain.value_objects.sku import Sku
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.utils.log_util import log


class CreateProductVariantUseCase:
    def __init__(
        self,
        variant_repository: ProductVariantRepository,
        product_repository: ProductRepository,
        t_shirt_size_repository: TShirtSizeRepository,
    ):
        self.variant_repository = variant_repository
        self.product_repository = product_repository
        self.t_shirt_size_repository = t_shirt_size_repository

    async def execute(self, payload: ProductVariantCreateRequest) -> ProductVariantResponse:
        try:
            sku = await self._resolve_sku(payload)
            variant_entity = to_product_variant_entity(payload, sku=sku)

            created_variant = await self.variant_repository.save(variant_entity)
            log.info(f"Product variant created with SKU: {created_variant.sku}")

            return to_product_variant_response(created_variant)

        except Exception as e:
            log.error(f"Unexpected error while saving product variant: {str(e)}")
            raise

    async def _resolve_sku(self, payload: ProductVariantCreateRequest) -> str:
        """Honor an explicit SKU and otherwise build one from the product catalog data."""
        if payload.sku and payload.sku.strip():
            return payload.sku.strip()

        try:
            product_uuid = UUID(payload.product_id)
        except ValueError:
            raise ValueError(f"Invalid product ID format: {payload.product_id}") from None

        product = await self.product_repository.find_by_id(product_uuid)
        if product is None:
            raise ValueError(f"Product not found with ID: {payload.product_id}")

        try:
            size_uuid = UUID(payload.size_id)
        except ValueError:
            raise ValueError(f"Invalid size ID format: {payload.size_id}") from None

        size = await self.t_shirt_size_repository.find_by_id(size_uuid)
        if size is None:
            raise ValueError(f"T-shirt size not found with ID: {payload.size_id}")

        return Sku.from_parts(product.name, str(size.size), payload.color).value
