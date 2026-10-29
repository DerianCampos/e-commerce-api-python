from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ProductResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    fit: str
    band_id: Optional[str] = None
    is_active: bool


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    description: Optional[str] = None
    fit: str
    band_id: Optional[str] = None
    is_active: bool = True


class ProductUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: Optional[str] = None
    description: Optional[str] = None
    fit: Optional[str] = None
    band_id: Optional[str] = None
    is_active: Optional[bool] = None
