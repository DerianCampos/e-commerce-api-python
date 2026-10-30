from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ProductBandResponse(BaseModel):
    """Band summary embedded in product read models."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    name: str
    country: Optional[str] = None
    genre: Optional[str] = None


class ProductVariantCatalogResponse(BaseModel):
    """Product variant as exposed by the storefront catalog."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    size_id: str
    size: Optional[str] = None
    color: str
    sku: str
    unit_price: Decimal
    stock_quantity: int


class ProductDetailResponse(BaseModel):
    """Product read model with its band and variants."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    fit: str
    image_url: Optional[str] = None
    is_active: bool
    band: Optional[ProductBandResponse] = None
    variants: list[ProductVariantCatalogResponse] = Field(default_factory=list)


class ProductResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    fit: str
    band_id: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    description: Optional[str] = None
    fit: str
    band_id: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True


class ProductUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: Optional[str] = None
    description: Optional[str] = None
    fit: Optional[str] = None
    band_id: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
