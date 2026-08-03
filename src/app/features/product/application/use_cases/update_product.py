from typing import Optional
from uuid import UUID

from src.app.features.product.application.dtos.product_dto import ProductResponse, ProductUpdateRequest
from src.app.features.product.application.mappers.product_mapper import to_product_response
from src.app.features.product.domain.exceptions.product_exception import ProductDoesNotExistException
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.features.product.domain.value_objects.fit import Fit
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id: str, product_update: ProductUpdateRequest) -> ProductResponse:

        try:
            product_uuid = UUID(product_id)
            product_entity_id = EntityId(product_uuid)

            existing_product = await self.product_repository.find_by_id(product_uuid)

            if not existing_product:
                log.warning(f"Cannot update product. Product not found with ID: {product_id}")
                raise ProductDoesNotExistException(product_entity_id)

            band_id: Optional[EntityId] = None
            if product_update.band_id is not None:
                band_id = EntityId.from_string(product_update.band_id)

            existing_product.update(
                name=product_update.name,
                description=product_update.description,
                fit=Fit.from_str(product_update.fit) if product_update.fit is not None else None,
                band_id=band_id,
                is_active=product_update.is_active,
            )

            updated_product = await self.product_repository.update(existing_product)

            log.info(f"Product with ID {product_id} successfully updated.")

            return to_product_response(updated_product)

        except ValueError as e:
            log.error(f"Invalid UUID format for product ID {product_id}: {e}")
            raise ValueError(f"Invalid product ID format: {product_id}")
        except ProductDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update product for {product_id}: {str(e)}")
            raise
