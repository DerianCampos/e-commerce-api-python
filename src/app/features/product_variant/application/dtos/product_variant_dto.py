from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    product_id: str
    size_id: str
    color: str
    sku: str
    unit_price: float
    stock_quantity: int


class ProductVariantCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    product_id: str
    size_id: str
    color: str = "black"
    sku: str
    unit_price: float
    stock_quantity: int = 0


class ProductVariantUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    color: str | None = None
    sku: str | None = None
    unit_price: float | None = None
    stock_quantity: int | None = None
