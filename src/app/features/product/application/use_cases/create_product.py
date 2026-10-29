from src.app.features.product.application.dtos.product_dto import ProductCreateRequest, ProductResponse
from src.app.features.product.application.mappers.product_mapper import to_product_entity, to_product_response
from src.app.features.product.domain.repositories.product_repository import ProductRepository
from src.app.shared.utils.log_util import log


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, payload: ProductCreateRequest) -> ProductResponse:
        try:
            product_entity = to_product_entity(payload)

            created_product = await self.product_repository.save(product_entity)
            log.info(f"Product created: {created_product.name}")

            response_dto = to_product_response(created_product)

            return response_dto

        except Exception as e:
            log.error(f"Unexpected error while saving product: {str(e)}")
            raise
