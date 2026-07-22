from decimal import Decimal

from src.app.features.product_variant.domain.entities.product_variant_entity import ProductVariantEntity
from src.app.features.product_variant.domain.value_objects.sku import Sku
from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductVariantModelMapper:
    @staticmethod
    def to_product_variant_model(variant_entity):
        return {
            "id": str(variant_entity.id.value),
            "product_id": str(variant_entity.product_id.value),
            "size_id": str(variant_entity.size_id.value),
            "color": variant_entity.color,
            "sku": variant_entity.sku.value,
            "unit_price": variant_entity.unit_price,
            "stock_quantity": variant_entity.stock_quantity,
            "created_at": variant_entity.created_at,
            "updated_at": variant_entity.updated_at,
        }

    @staticmethod
    def to_product_variant_entity(variant_model):
        if variant_model is None:
            return None
        return ProductVariantEntity(
            id=EntityId(variant_model.id),
            product_id=EntityId(variant_model.product_id),
            size_id=EntityId(variant_model.size_id),
            color=variant_model.color,
            sku=Sku(variant_model.sku),
            unit_price=Decimal(str(variant_model.unit_price)),
            stock_quantity=variant_model.stock_quantity,
            created_at=variant_model.created_at,
            updated_at=variant_model.updated_at,
        )
