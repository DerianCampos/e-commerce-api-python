from fastapi import Depends

from src.app.composition.repositories import (
    get_band_repository,
    get_product_repository,
    get_product_variant_repository,
    get_t_shirt_size_repository,
)
from src.app.features.band.infrastructure.repository.band_repository_impl import BandRepositoryImpl
from src.app.features.product.application.use_cases.create_product import CreateProductUseCase
from src.app.features.product.application.use_cases.delete_product import DeleteProductUseCase
from src.app.features.product.application.use_cases.get_product_by_id import GetProductByIdUseCase
from src.app.features.product.application.use_cases.list_products import ListProductsUseCase
from src.app.features.product.application.use_cases.update_product import UpdateProductUseCase
from src.app.features.product.infrastructure.repository.product_repository_impl import ProductRepositoryImpl
from src.app.features.product_variant.infrastructure.repository.product_variant_repository_impl import (
    ProductVariantRepositoryImpl,
)
from src.app.features.t_shirt_size.infrastructure.repository.t_shirt_size_repository_impl import (
    TShirtSizeRepositoryImpl,
)


async def get_create_product_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
) -> CreateProductUseCase:
    return CreateProductUseCase(repo)


async def get_get_product_by_id_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
    product_variant_repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
    band_repo: BandRepositoryImpl = Depends(get_band_repository),
    t_shirt_size_repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> GetProductByIdUseCase:
    return GetProductByIdUseCase(repo, product_variant_repo, band_repo, t_shirt_size_repo)


async def get_update_product_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
) -> UpdateProductUseCase:
    return UpdateProductUseCase(repo)


async def get_delete_product_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
) -> DeleteProductUseCase:
    return DeleteProductUseCase(repo)


async def get_list_products_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
    product_variant_repo: ProductVariantRepositoryImpl = Depends(get_product_variant_repository),
    band_repo: BandRepositoryImpl = Depends(get_band_repository),
    t_shirt_size_repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> ListProductsUseCase:
    return ListProductsUseCase(repo, product_variant_repo, band_repo, t_shirt_size_repo)
