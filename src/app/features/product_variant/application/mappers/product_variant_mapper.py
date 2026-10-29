from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from src.app.features.product_variant.application.dtos.product_variant_dto import (
    ProductVariantCreateRequest,
    ProductVariantResponse,
)
from src.app.features.product_variant.domain.entities.product_variant_entity import ProductVariantEntity
from src.app.features.product_variant.domain.value_objects.sku import Sku
from src.app.shared.domain.value_objects.entity_id import EntityId


def to_product_variant_response(variant_entity: Union[BaseModel, ProductVariantEntity]) -> ProductVariantResponse:
    return ProductVariantResponse(
        id=str(variant_entity.id.value),
        product_id=str(variant_entity.product_id.value),
        size_id=str(variant_entity.size_id.value),
        color=variant_entity.color,
        sku=str(variant_entity.sku.value),
        unit_price=float(variant_entity.unit_price),
        stock_quantity=int(variant_entity.stock_quantity),
    )


def to_product_variant_entity(variant_dto: ProductVariantCreateRequest) -> ProductVariantEntity:
    return ProductVariantEntity.create(
        product_id=EntityId.from_string(variant_dto.product_id),
        size_id=EntityId.from_string(variant_dto.size_id),
        color=variant_dto.color,
        sku=Sku(variant_dto.sku),
        unit_price=Decimal(str(variant_dto.unit_price)),
        stock_quantity=variant_dto.stock_quantity,
    )
