from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    updated_at: Optional[str]

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[Decimal]
