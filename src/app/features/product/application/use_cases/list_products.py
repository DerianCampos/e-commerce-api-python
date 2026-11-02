from typing import Optional
from uuid import UUID

from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.features.product.application.dtos.product_dto import ProductDetailResponse
from src.app.features.product.application.mappers.product_mapper import to_product_detail_response
from src.app.features.product.domain.entities.product_entity import ProductEntity
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.application.dtos.pagination_dto import PaginatedResponse
from src.app.shared.utils.log_util import log


class ListProductsUseCase:
    """
    Storefront product listing: paginated products enriched with band and variants.
    """

    def __init__(
        self,
        product_repository: ProductRepository,
        product_variant_repository: ProductVariantRepository,
        band_repository: BandRepository,
        t_shirt_size_repository: TShirtSizeRepository,
    ):
        self.product_repository = product_repository
        self.product_variant_repository = product_variant_repository
        self.band_repository = band_repository
        self.t_shirt_size_repository = t_shirt_size_repository

    async def execute(
        self,
        page: int = 1,
        per_page: int = 20,
        band_id: Optional[str] = None,
        q: Optional[str] = None,
        order: Optional[str] = None,
    ) -> PaginatedResponse[ProductDetailResponse]:
        try:
            if order not in (None, "latest", "oldest"):
                raise ValueError(f"Unsupported order: {order}")

            band_uuid = UUID(band_id) if band_id else None
            normalized_q = q.strip() if q else None

            total = await self.product_repository.count_all(band_id=band_uuid, q=normalized_q)
            products = await self.product_repository.find_all(
                limit=per_page,
                offset=(page - 1) * per_page,
                band_id=band_uuid,
                q=normalized_q,
                newest_first=order == "latest",
            )

            items = await self._to_detail_responses(products)

            log.info(f"Listed {len(items)} products (page {page}, total {total}).")

            return PaginatedResponse(total=total, page=page, per_page=per_page, items=items)

        except ValueError:
            raise
        except Exception as e:
            log.error(f"Unexpected error during list products: {str(e)}")
            raise

    async def _to_detail_responses(self, products: list[ProductEntity]) -> list[ProductDetailResponse]:
        product_ids = [product.id.value for product in products]
        band_ids = {product.band_id.value for product in products if product.band_id}

        variants = await self.product_variant_repository.find_by_product_ids(product_ids)
        bands = await self.band_repository.find_by_ids(list(band_ids))
        sizes = await self.t_shirt_size_repository.find_all()

        bands_by_id = {str(band.id.value): band for band in bands}
        sizes_by_id = {str(size.id.value): str(size.size) for size in sizes}

        variants_by_product: dict[str, list] = {}
        for variant in variants:
            variants_by_product.setdefault(str(variant.product_id.value), []).append(variant)

        return [
            to_product_detail_response(
                product,
                band=bands_by_id.get(str(product.band_id.value)) if product.band_id else None,
                variants=variants_by_product.get(str(product.id.value), []),
                sizes_by_id=sizes_by_id,
            )
            for product in products
        ]
