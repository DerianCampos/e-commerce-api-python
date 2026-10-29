from decimal import Decimal
from secrets import token_hex
from typing import Optional, Union

from pydantic import BaseModel

from src.app.features.order.application.dtos.order_dto import OrderCreateRequest, OrderResponse
from src.app.features.order.domain.entities.order_entity import OrderEntity
from src.app.features.order.domain.value_objects.order_status import OrderStatus
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.date_util import get_current_date


def generate_order_number() -> str:
    """
    Generate a unique order number in the format ORD-YYYYMMDD-XXXXXX.
    """
    return f"ORD-{get_current_date().replace('-', '')}-{token_hex(3).upper()}"


def to_order_response(order_entity: Union[BaseModel, OrderEntity]) -> OrderResponse:
    return OrderResponse(
        id=str(order_entity.id.value),
        user_id=str(order_entity.user_id.value) if order_entity.user_id else None,
        order_number=order_entity.order_number,
        status=str(order_entity.status),
        total_amount=float(order_entity.total_amount),
        currency=order_entity.currency,
        shipping_address=order_entity.shipping_address,
        billing_address=order_entity.billing_address,
    )


def to_order_entity(order_dto: OrderCreateRequest) -> OrderEntity:
    user_id: Optional[EntityId] = None
    if order_dto.user_id:
        user_id = EntityId.from_string(order_dto.user_id)

    return OrderEntity.create(
        user_id=user_id,
        order_number=generate_order_number(),
        status=OrderStatus.from_str(order_dto.status),
        total_amount=Decimal(str(order_dto.total_amount)),
        currency=order_dto.currency,
        shipping_address=order_dto.shipping_address,
        billing_address=order_dto.billing_address,
    )
