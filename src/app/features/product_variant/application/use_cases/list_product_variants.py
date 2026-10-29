from typing import List, Optional

from src.app.features.product_variant.application.dtos.product_variant_dto import ProductVariantResponse
from src.app.features.product_variant.application.mappers.product_variant_mapper import to_product_variant_response
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.shared.utils.log_util import log


class ListProductVariantsUseCase:
    def __init__(self, variant_repository: ProductVariantRepository):
        self.variant_repository = variant_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[ProductVariantResponse]:
        try:
            variants = await self.variant_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(variants)} product variants.")

            return [to_product_variant_response(v) for v in variants]

        except Exception as e:
            log.error(f"Unexpected error during list product variants: {str(e)}")
            raise
