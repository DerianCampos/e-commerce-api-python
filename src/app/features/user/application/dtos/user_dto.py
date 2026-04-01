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
    email: str
    full_name: str
    role: str
    is_active: bool

class UserCreate(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"
    is_active: bool = True


class UserUpdate(BaseModel):
    """
    DTO for partial user updates.
    All fields are optional - only provided fields will be updated.
    Note: role and is_active are managed via admin-only endpoints.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

