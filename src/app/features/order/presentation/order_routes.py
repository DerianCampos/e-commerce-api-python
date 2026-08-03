from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.orders import (
    get_create_order_use_case,
    get_delete_order_use_case,
    get_get_order_by_id_use_case,
    get_list_orders_use_case,
    get_update_order_use_case,
)
from src.app.features.order.application.dtos.order_dto import (
    OrderCreateRequest,
    OrderResponse,
    OrderUpdateRequest,
)
from src.app.features.order.application.use_cases.create_order import CreateOrderUseCase
from src.app.features.order.application.use_cases.delete_order import DeleteOrderUseCase
from src.app.features.order.application.use_cases.get_order_by_id import GetOrderByIdUseCase
from src.app.features.order.application.use_cases.list_orders import ListOrdersUseCase
from src.app.features.order.application.use_cases.update_order import UpdateOrderUseCase
from src.app.features.order.domain.exceptions.order_exception import OrderDoesNotExistException

router = APIRouter()


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def list_orders(
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    use_case: ListOrdersUseCase = Depends(get_list_orders_use_case),
) -> List[OrderResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order_by_id(
    order_id: str,
    use_case: GetOrderByIdUseCase = Depends(get_get_order_by_id_use_case),
) -> OrderResponse:
    try:
        return await use_case.execute(order_id)
    except OrderDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreateRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> OrderResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An order with this number already exists.")
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order(
    order_id: str,
    payload: OrderUpdateRequest,
    use_case: UpdateOrderUseCase = Depends(get_update_order_use_case),
) -> OrderResponse:
    try:
        return await use_case.execute(order_id, payload)
    except OrderDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: str,
    use_case: DeleteOrderUseCase = Depends(get_delete_order_use_case),
) -> None:
    try:
        await use_case.execute(order_id)
    except OrderDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
