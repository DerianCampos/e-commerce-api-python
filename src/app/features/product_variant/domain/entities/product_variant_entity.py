from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.app.features.product_variant.domain.value_objects.sku import Sku
from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductVariantEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        product_id: EntityId,
        size_id: EntityId,
        color: str,
        sku: Sku,
        unit_price: Decimal,
        stock_quantity: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._product_id = product_id
        self._size_id = size_id
        self._color = color
        self._sku = sku
        self._unit_price = unit_price
        self._stock_quantity = stock_quantity
        super().__init__(id, created_at, updated_at)

    @property
    def product_id(self) -> EntityId:
        return self._product_id

    @property
    def size_id(self) -> EntityId:
        return self._size_id

    @property
    def color(self) -> str:
        return self._color

    @property
    def sku(self) -> Sku:
        return self._sku

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @classmethod
    def create(
        cls,
        product_id: EntityId,
        size_id: EntityId,
        color: str,
        sku: Sku,
        unit_price: Decimal,
        stock_quantity: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "ProductVariantEntity":
        return cls(
            id=EntityId.generate(),
            product_id=product_id,
            size_id=size_id,
            color=color,
            sku=sku,
            unit_price=unit_price,
            stock_quantity=stock_quantity,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        color: Optional[str] = None,
        sku: Optional[Sku] = None,
        unit_price: Optional[Decimal] = None,
        stock_quantity: Optional[int] = None,
    ) -> None:
        if color is not None:
            self._color = color
        if sku is not None:
            self._sku = sku
        if unit_price is not None:
            self._unit_price = unit_price
        if stock_quantity is not None:
            self._stock_quantity = stock_quantity
        self.mark_as_updated()
