from typing import Optional, Union

from pydantic import BaseModel

from src.app.features.band.domain.entities.band_entity import BandEntity
from src.app.features.product.application.dtos.product_dto import (
    ProductBandResponse,
    ProductCreateRequest,
    ProductDetailResponse,
    ProductResponse,
    ProductVariantCatalogResponse,
)
from src.app.features.product.domain.entities.product_entity import ProductEntity
from src.app.features.product.domain.value_objects.fit import Fit
from src.app.features.product_variant.domain.entities.product_variant_entity import ProductVariantEntity
from src.app.features.t_shirt_size.domain.value_objects.size import Size
from src.app.shared.domain.value_objects.entity_id import EntityId

_SIZE_RANK = {size.value: index for index, size in enumerate(Size)}


def to_product_response(product_entity: Union[BaseModel, ProductEntity]) -> ProductResponse:
    return ProductResponse(
        id=str(product_entity.id.value),
        name=product_entity.name,
        description=product_entity.description,
        fit=str(product_entity.fit.value),
        band_id=str(product_entity.band_id.value) if product_entity.band_id else None,
        image_url=product_entity.image_url,
        is_active=bool(product_entity.is_active),
    )


def to_product_detail_response(
    product: ProductEntity,
    band: Optional[BandEntity] = None,
    variants: Optional[list[ProductVariantEntity]] = None,
    sizes_by_id: Optional[dict[str, str]] = None,
) -> ProductDetailResponse:
    sizes = sizes_by_id or {}

    catalog_variants = [
        ProductVariantCatalogResponse(
            id=str(variant.id.value),
            size_id=str(variant.size_id.value),
            size=sizes.get(str(variant.size_id.value)),
            color=variant.color,
            sku=str(variant.sku.value),
            unit_price=variant.unit_price,
            stock_quantity=int(variant.stock_quantity),
        )
        for variant in variants or []
    ]
    catalog_variants.sort(
        key=lambda variant: _SIZE_RANK.get(variant.size or "", len(_SIZE_RANK)),
    )

    return ProductDetailResponse(
        id=str(product.id.value),
        name=product.name,
        description=product.description,
        fit=str(product.fit.value),
        image_url=product.image_url,
        is_active=bool(product.is_active),
        band=ProductBandResponse(
            id=str(band.id.value),
            name=band.name,
            country=band.country,
            genre=band.genre,
        )
        if band
        else None,
        variants=catalog_variants,
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
        image_url=product_dto.image_url,
    )
