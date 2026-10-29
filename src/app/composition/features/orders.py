from fastapi import Depends

from src.app.composition.repositories import get_order_repository
from src.app.features.order.application.use_cases.create_order import CreateOrderUseCase
from src.app.features.order.application.use_cases.delete_order import DeleteOrderUseCase
from src.app.features.order.application.use_cases.get_order_by_id import GetOrderByIdUseCase
from src.app.features.order.application.use_cases.list_orders import ListOrdersUseCase
from src.app.features.order.application.use_cases.update_order import UpdateOrderUseCase
from src.app.features.order.infrastructure.repository.order_repository_impl import OrderRepositoryImpl


async def get_create_order_use_case(
    repo: OrderRepositoryImpl = Depends(get_order_repository),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(repo)


async def get_get_order_by_id_use_case(
    repo: OrderRepositoryImpl = Depends(get_order_repository),
) -> GetOrderByIdUseCase:
    return GetOrderByIdUseCase(repo)


async def get_update_order_use_case(
    repo: OrderRepositoryImpl = Depends(get_order_repository),
) -> UpdateOrderUseCase:
    return UpdateOrderUseCase(repo)


async def get_delete_order_use_case(
    repo: OrderRepositoryImpl = Depends(get_order_repository),
) -> DeleteOrderUseCase:
    return DeleteOrderUseCase(repo)


async def get_list_orders_use_case(
    repo: OrderRepositoryImpl = Depends(get_order_repository),
) -> ListOrdersUseCase:
    return ListOrdersUseCase(repo)
