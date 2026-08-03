from decimal import Decimal

from src.app.features.order_item.domain.entities.order_item_entity import OrderItemEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderItemModelMapper:
    @staticmethod
    def to_order_item_model(order_item_entity):
        return {
            "id": str(order_item_entity.id.value),
            "order_id": str(order_item_entity.order_id.value),
            "product_variant_id": str(order_item_entity.product_variant_id.value),
            "product_name": order_item_entity.product_name,
            "band_name": order_item_entity.band_name,
            "size": order_item_entity.size,
            "color": order_item_entity.color,
            "sku": order_item_entity.sku,
            "unit_price": order_item_entity.unit_price,
            "quantity": order_item_entity.quantity,
            "line_total": order_item_entity.line_total,
            "created_at": order_item_entity.created_at,
            "updated_at": order_item_entity.updated_at,
        }

    @staticmethod
    def to_order_item_entity(order_item_model):
        if order_item_model is None:
            return None
        return OrderItemEntity(
            id=EntityId(order_item_model.id),
            order_id=EntityId(order_item_model.order_id),
            product_variant_id=EntityId(order_item_model.product_variant_id),
            product_name=order_item_model.product_name,
            band_name=order_item_model.band_name,
            size=order_item_model.size,
            color=order_item_model.color,
            sku=order_item_model.sku,
            unit_price=Decimal(str(order_item_model.unit_price)),
            quantity=order_item_model.quantity,
            line_total=Decimal(str(order_item_model.line_total)),
            created_at=order_item_model.created_at,
            updated_at=order_item_model.updated_at,
        )
