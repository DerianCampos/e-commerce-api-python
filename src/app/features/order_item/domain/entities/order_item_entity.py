from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderItemEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        order_id: EntityId,
        product_variant_id: EntityId,
        product_name: str,
        band_name: Optional[str],
        size: str,
        color: str,
        sku: str,
        unit_price: Decimal,
        quantity: int,
        line_total: Decimal,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._order_id = order_id
        self._product_variant_id = product_variant_id
        self._product_name = product_name
        self._band_name = band_name
        self._size = size
        self._color = color
        self._sku = sku
        self._unit_price = unit_price
        self._quantity = quantity
        self._line_total = line_total
        super().__init__(id, created_at, updated_at)

    @property
    def order_id(self) -> EntityId:
        return self._order_id

    @property
    def product_variant_id(self) -> EntityId:
        return self._product_variant_id

    @property
    def product_name(self) -> str:
        return self._product_name

    @property
    def band_name(self) -> Optional[str]:
        return self._band_name

    @property
    def size(self) -> str:
        return self._size

    @property
    def color(self) -> str:
        return self._color

    @property
    def sku(self) -> str:
        return self._sku

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def line_total(self) -> Decimal:
        return self._line_total

    @classmethod
    def create(
        cls,
        order_id: EntityId,
        product_variant_id: EntityId,
        product_name: str,
        band_name: Optional[str],
        size: str,
        color: str,
        sku: str,
        unit_price: Decimal,
        quantity: int,
        line_total: Decimal,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "OrderItemEntity":
        return cls(
            id=EntityId.generate(),
            order_id=order_id,
            product_variant_id=product_variant_id,
            product_name=product_name,
            band_name=band_name,
            size=size,
            color=color,
            sku=sku,
            unit_price=unit_price,
            quantity=quantity,
            line_total=line_total,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        product_name: Optional[str] = None,
        band_name: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        sku: Optional[str] = None,
        unit_price: Optional[Decimal] = None,
        quantity: Optional[int] = None,
    ) -> None:
        if product_name is not None:
            self._product_name = product_name
        if band_name is not None:
            self._band_name = band_name
        if size is not None:
            self._size = size
        if color is not None:
            self._color = color
        if sku is not None:
            self._sku = sku
        if unit_price is not None:
            self._unit_price = unit_price
        if quantity is not None:
            self._quantity = quantity
        self._line_total = self._unit_price * self._quantity
        self.mark_as_updated()
