from fastapi import Depends

from src.app.composition.repositories import get_product_repository
from src.app.features.product.application.use_cases.create_product import CreateProductUseCase
from src.app.features.product.application.use_cases.delete_product import DeleteProductUseCase
from src.app.features.product.application.use_cases.get_product_by_id import GetProductByIdUseCase
from src.app.features.product.application.use_cases.list_products import ListProductsUseCase
from src.app.features.product.application.use_cases.update_product import UpdateProductUseCase
from src.app.features.product.infrastructure.repository.product_repository_impl import ProductRepositoryImpl


async def get_create_product_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
) -> CreateProductUseCase:
    return CreateProductUseCase(repo)


async def get_get_product_by_id_use_case(
    repo: ProductRepositoryImpl = Depends(get_product_repository),
) -> GetProductByIdUseCase:
    return GetProductByIdUseCase(repo)


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
) -> ListProductsUseCase:
    return ListProductsUseCase(repo)
