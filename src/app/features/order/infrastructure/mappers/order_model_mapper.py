from decimal import Decimal

from src.app.features.order.domain.entities.order_entity import OrderEntity
from src.app.features.order.domain.value_objects.order_status import OrderStatus
from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderModelMapper:
    @staticmethod
    def to_order_model(order_entity):
        return {
            "id": str(order_entity.id.value),
            "user_id": str(order_entity.user_id.value) if order_entity.user_id else None,
            "order_number": order_entity.order_number,
            "status": str(order_entity.status),
            "total_amount": order_entity.total_amount,
            "currency": order_entity.currency,
            "shipping_address": order_entity.shipping_address,
            "billing_address": order_entity.billing_address,
            "created_at": order_entity.created_at,
            "updated_at": order_entity.updated_at,
        }

    @staticmethod
    def to_order_entity(order_model):
        if order_model is None:
            return None
        return OrderEntity(
            id=EntityId(order_model.id),
            user_id=EntityId(order_model.user_id) if order_model.user_id else None,
            order_number=order_model.order_number,
            status=OrderStatus.from_str(order_model.status),
            total_amount=Decimal(str(order_model.total_amount)),
            currency=order_model.currency,
            shipping_address=order_model.shipping_address,
            billing_address=order_model.billing_address,
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
        )
