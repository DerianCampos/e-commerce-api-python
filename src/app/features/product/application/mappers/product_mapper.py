from typing import Optional, Union

from pydantic import BaseModel

from src.app.features.product.application.dtos.product_dto import ProductCreateRequest, ProductResponse
from src.app.features.product.domain.entities.product_entity import ProductEntity
from src.app.features.product.domain.value_objects.fit import Fit
from src.app.shared.domain.value_objects.entity_id import EntityId


def to_product_response(product_entity: Union[BaseModel, ProductEntity]) -> ProductResponse:
    return ProductResponse(
        id=str(product_entity.id.value),
        name=product_entity.name,
        description=product_entity.description,
        fit=str(product_entity.fit.value),
        band_id=str(product_entity.band_id.value) if product_entity.band_id else None,
        is_active=bool(product_entity.is_active),
    )


def to_product_entity(product_dto: ProductCreateRequest) -> ProductEntity:
    band_id: Optional[EntityId] = None
    if product_dto.band_id:
        band_id = EntityId.from_string(product_dto.band_id)

    return ProductEntity.create(
        name=product_dto.name,
        description=product_dto.description,
        fit=Fit.from_str(product_dto.fit),
        band_id=band_id,
        is_active=product_dto.is_active,
    )
