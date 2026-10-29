from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    order_id: str
    product_variant_id: str
    product_name: str
    band_name: Optional[str] = None
    size: str
    color: str
    sku: str
    unit_price: float
    quantity: int
    line_total: float


class OrderItemCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    order_id: str
    product_variant_id: str
    product_name: str
    band_name: Optional[str] = None
    size: str
    color: str
    sku: str
    unit_price: float
    quantity: int = 1


class OrderItemUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    product_name: Optional[str] = None
    band_name: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    sku: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
