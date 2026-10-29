from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class OrderResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    user_id: Optional[str] = None
    order_number: str
    status: str
    total_amount: float
    currency: str
    shipping_address: Optional[dict] = None
    billing_address: Optional[dict] = None


class OrderCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: Optional[str] = None
    status: str = "pending"
    total_amount: float = 0
    currency: str = "USD"
    shipping_address: Optional[dict] = None
    billing_address: Optional[dict] = None


class OrderUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    shipping_address: Optional[dict] = None
    billing_address: Optional[dict] = None
