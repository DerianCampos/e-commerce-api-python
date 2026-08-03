from fastapi import Depends

from src.app.composition.repositories import get_product_variant_repository
from src.app.features.product_variant.application.use_cases.create_product_variant import CreateProductVariantUseCase
from src.app.features.product_variant.application.use_cases.delete_product_variant import DeleteProductVariantUseCase
from src.app.features.product_variant.application.use_cases.get_product_variant_by_id import (
    GetProductVariantByIdUseCase,
)
from src.app.features.product_variant.application.use_cases.list_product_variants import ListProductVariantsUseCase
from src.app.features.product_variant.application.use_cases.update_product_variant import UpdateProductVariantUseCase
from src.app.features.product_variant.infrastructure.repository.product_variant_repository_impl import (
    ProductVariantRepositoryImpl,
)


async def get_create_product_variant_use_case(
    repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
) -> CreateProductVariantUseCase:
    return CreateProductVariantUseCase(repo)


async def get_get_product_variant_by_id_use_case(
    repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
) -> GetProductVariantByIdUseCase:
    return GetProductVariantByIdUseCase(repo)


async def get_update_product_variant_use_case(
    repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
) -> UpdateProductVariantUseCase:
    return UpdateProductVariantUseCase(repo)


async def get_delete_product_variant_use_case(
    repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
) -> DeleteProductVariantUseCase:
    return DeleteProductVariantUseCase(repo)


async def get_list_product_variants_use_case(
    repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
) -> ListProductVariantsUseCase:
    return ListProductVariantsUseCase(repo)
