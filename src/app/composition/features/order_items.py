from fastapi import Depends

from src.app.composition.repositories import get_order_item_repository
from src.app.features.order_item.application.use_cases.create_order_item import CreateOrderItemUseCase
from src.app.features.order_item.application.use_cases.delete_order_item import DeleteOrderItemUseCase
from src.app.features.order_item.application.use_cases.get_order_item_by_id import GetOrderItemByIdUseCase
from src.app.features.order_item.application.use_cases.list_order_items import ListOrderItemsUseCase
from src.app.features.order_item.application.use_cases.update_order_item import UpdateOrderItemUseCase
from src.app.features.order_item.infrastructure.repository.order_item_repository_impl import OrderItemRepositoryImpl


async def get_create_order_item_use_case(
    repo: OrderItemRepositoryImpl = Depends(get_order_item_repository),
) -> CreateOrderItemUseCase:
    return CreateOrderItemUseCase(repo)


async def get_get_order_item_by_id_use_case(
    repo: OrderItemRepositoryImpl = Depends(get_order_item_repository),
) -> GetOrderItemByIdUseCase:
    return GetOrderItemByIdUseCase(repo)


async def get_update_order_item_use_case(
    repo: OrderItemRepositoryImpl = Depends(get_order_item_repository),
) -> UpdateOrderItemUseCase:
    return UpdateOrderItemUseCase(repo)


async def get_delete_order_item_use_case(
    repo: OrderItemRepositoryImpl = Depends(get_order_item_repository),
) -> DeleteOrderItemUseCase:
    return DeleteOrderItemUseCase(repo)


async def get_list_order_items_use_case(
    repo: OrderItemRepositoryImpl = Depends(get_order_item_repository),
) -> ListOrderItemsUseCase:
    return ListOrderItemsUseCase(repo)
