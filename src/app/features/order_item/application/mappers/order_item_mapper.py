from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from src.app.features.order_item.application.dtos.order_item_dto import OrderItemCreateRequest, OrderItemResponse
from src.app.features.order_item.domain.entities.order_item_entity import OrderItemEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


def to_order_item_response(order_item_entity: Union[BaseModel, OrderItemEntity]) -> OrderItemResponse:
    return OrderItemResponse(
        id=str(order_item_entity.id.value),
        order_id=str(order_item_entity.order_id.value),
        product_variant_id=str(order_item_entity.product_variant_id.value),
        product_name=order_item_entity.product_name,
        band_name=order_item_entity.band_name,
        size=order_item_entity.size,
        color=order_item_entity.color,
        sku=order_item_entity.sku,
        unit_price=float(order_item_entity.unit_price),
        quantity=int(order_item_entity.quantity),
        line_total=float(order_item_entity.line_total),
    )


def to_order_item_entity(order_item_dto: OrderItemCreateRequest) -> OrderItemEntity:
    unit_price = Decimal(str(order_item_dto.unit_price))
    quantity = order_item_dto.quantity
    line_total = unit_price * quantity

    return OrderItemEntity.create(
        order_id=EntityId.from_string(order_item_dto.order_id),
        product_variant_id=EntityId.from_string(order_item_dto.product_variant_id),
        product_name=order_item_dto.product_name,
        band_name=order_item_dto.band_name,
        size=order_item_dto.size,
        color=order_item_dto.color,
        sku=order_item_dto.sku,
        unit_price=unit_price,
        quantity=quantity,
        line_total=line_total,
    )
