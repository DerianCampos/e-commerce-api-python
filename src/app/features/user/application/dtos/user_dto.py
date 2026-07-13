from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class UserResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

    id: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_active: bool

class UserCreateRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    is_active: bool = True


class UserUpdateRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

