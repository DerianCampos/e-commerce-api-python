from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.composition.infrastructure import get_database_session
from src.app.features.band.infrastructure.repository.band_repository_impl import BandRepositoryImpl
from src.app.features.order.infrastructure.repository.order_repository_impl import OrderRepositoryImpl
from src.app.features.order_item.infrastructure.repository.order_item_repository_impl import OrderItemRepositoryImpl
from src.app.features.product.infrastructure.repository.product_repository_impl import ProductRepositoryImpl
from src.app.features.product_variant.infrastructure.repository.product_variant_repository_impl import (
    ProductVariantRepositoryImpl,
)
from src.app.features.t_shirt_size.infrastructure.repository.t_shirt_size_repository_impl import (
    TShirtSizeRepositoryImpl,
)
from src.app.features.user.infrastructure.repository.user_repository_impl import UserRepositoryImpl


async def get_user_repository(
        session: AsyncSession = Depends(get_database_session)
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)

async def get_band_repository(
        session: AsyncSession = Depends(get_database_session)
) -> BandRepositoryImpl:
    return BandRepositoryImpl(session)

async def get_product_repository(
        session: AsyncSession = Depends(get_database_session)
) -> ProductRepositoryImpl:
    return ProductRepositoryImpl(session)

async def get_product_variant_repository(
        session: AsyncSession = Depends(get_database_session)
) -> ProductVariantRepositoryImpl:
    return ProductVariantRepositoryImpl(session)

async def get_t_shirt_size_repository(
        session: AsyncSession = Depends(get_database_session)
) -> TShirtSizeRepositoryImpl:
    return TShirtSizeRepositoryImpl(session)

async def get_order_repository(
        session: AsyncSession = Depends(get_database_session)
) -> OrderRepositoryImpl:
    return OrderRepositoryImpl(session)

async def get_order_item_repository(
        session: AsyncSession = Depends(get_database_session)
) -> OrderItemRepositoryImpl:
    return OrderItemRepositoryImpl(session)
