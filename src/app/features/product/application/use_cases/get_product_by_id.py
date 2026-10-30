from uuid import UUID

from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.features.product.application.dtos.product_dto import ProductDetailResponse
from src.app.features.product.application.mappers.product_mapper import to_product_detail_response
from src.app.features.product.domain.exceptions.product_exception import ProductDoesNotExistException
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.features.product_variant.domain.repositories.product_variant_repository import ProductVariantRepository
from src.app.features.t_shirt_size.domain.repositories.t_shirt_size_repository import TShirtSizeRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetProductByIdUseCase:
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

    async def execute(self, product_id: str) -> ProductDetailResponse:
        try:
            product_uuid = UUID(product_id)

            existing_product = await self.product_repository.find_by_id(product_uuid)

            if not existing_product:
                log.warning(f"Product not found with ID: {product_id}")
                raise ProductDoesNotExistException(EntityId(product_uuid))

            variants = await self.product_variant_repository.find_by_product_id(product_uuid)
            band = (
                await self.band_repository.find_by_id(existing_product.band_id.value)
                if existing_product.band_id
                else None
            )
            sizes = await self.t_shirt_size_repository.find_all()
            sizes_by_id = {str(size.id.value): str(size.size) for size in sizes}

            return to_product_detail_response(
                existing_product,
                band=band,
                variants=variants,
                sizes_by_id=sizes_by_id,
            )

        except ValueError as e:
            log.error(f"Invalid UUID format for product ID {product_id}: {e}")
            raise ValueError(f"Invalid product ID format: {product_id}")
        except ProductDoesNotExistException:
            log.error(f"Product does not exist with ID: {product_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get product by ID for {product_id}: {str(e)}")
            raise
