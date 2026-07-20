from src.app.features.product.domain.entities.product_entity import ProductEntity
from src.app.features.product.domain.value_objects.fit import Fit
from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductModelMapper:
    @staticmethod
    def to_product_model(product_entity):
        return {
            "id": str(product_entity.id.value),
            "name": product_entity.name,
            "description": product_entity.description,
            "fit": product_entity.fit.value,
            "band_id": str(product_entity.band_id.value) if product_entity.band_id else None,
            "is_active": product_entity.is_active,
            "created_at": product_entity.created_at,
            "updated_at": product_entity.updated_at,
        }

    @staticmethod
    def to_product_entity(product_model):
        if product_model is None:
            return None
        return ProductEntity(
            id=EntityId(product_model.id),
            name=product_model.name,
            description=product_model.description,
            fit=Fit.from_str(product_model.fit),
            band_id=EntityId(product_model.band_id) if product_model.band_id else None,
            is_active=product_model.is_active,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at,
        )
