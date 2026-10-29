from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class TShirtSizeResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)

    id: str
    size: str
    chest_min_cm: Optional[int] = None
    chest_max_cm: Optional[int] = None


class TShirtSizeCreateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    size: str
    chest_min_cm: Optional[int] = None
    chest_max_cm: Optional[int] = None


class TShirtSizeUpdateRequest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    size: Optional[str] = None
    chest_min_cm: Optional[int] = None
    chest_max_cm: Optional[int] = None
