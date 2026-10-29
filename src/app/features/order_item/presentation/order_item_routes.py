from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.order_items import (
    get_create_order_item_use_case,
    get_delete_order_item_use_case,
    get_get_order_item_by_id_use_case,
    get_list_order_items_use_case,
    get_update_order_item_use_case,
)
from src.app.features.order_item.application.dtos.order_item_dto import (
    OrderItemCreateRequest,
    OrderItemResponse,
    OrderItemUpdateRequest,
)
from src.app.features.order_item.application.use_cases.create_order_item import CreateOrderItemUseCase
from src.app.features.order_item.application.use_cases.delete_order_item import DeleteOrderItemUseCase
from src.app.features.order_item.application.use_cases.get_order_item_by_id import GetOrderItemByIdUseCase
from src.app.features.order_item.application.use_cases.list_order_items import ListOrderItemsUseCase
from src.app.features.order_item.application.use_cases.update_order_item import UpdateOrderItemUseCase
from src.app.features.order_item.domain.exceptions.order_item_exception import OrderItemDoesNotExistException

router = APIRouter()


@router.get("/", response_model=List[OrderItemResponse], status_code=status.HTTP_200_OK)
async def list_order_items(
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    use_case: ListOrderItemsUseCase = Depends(get_list_order_items_use_case),
) -> List[OrderItemResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{order_item_id}", response_model=OrderItemResponse, status_code=status.HTTP_200_OK)
async def get_order_item_by_id(
    order_item_id: str,
    use_case: GetOrderItemByIdUseCase = Depends(get_get_order_item_by_id_use_case),
) -> OrderItemResponse:
    try:
        return await use_case.execute(order_item_id)
    except OrderItemDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
async def create_order_item(
    payload: OrderItemCreateRequest,
    use_case: CreateOrderItemUseCase = Depends(get_create_order_item_use_case),
) -> OrderItemResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order item already exists.")
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{order_item_id}", response_model=OrderItemResponse, status_code=status.HTTP_200_OK)
async def update_order_item(
    order_item_id: str,
    payload: OrderItemUpdateRequest,
    use_case: UpdateOrderItemUseCase = Depends(get_update_order_item_use_case),
) -> OrderItemResponse:
    try:
        return await use_case.execute(order_item_id, payload)
    except OrderItemDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_item(
    order_item_id: str,
    use_case: DeleteOrderItemUseCase = Depends(get_delete_order_item_use_case),
) -> None:
    try:
        await use_case.execute(order_item_id)
    except OrderItemDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
