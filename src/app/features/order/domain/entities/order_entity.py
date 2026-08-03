from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.app.features.order.domain.value_objects.order_status import OrderStatus
from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        user_id: Optional[EntityId],
        order_number: str,
        status: OrderStatus,
        total_amount: Decimal,
        currency: str,
        shipping_address: Optional[dict],
        billing_address: Optional[dict],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._user_id = user_id
        self._order_number = order_number
        self._status = status
        self._total_amount = total_amount
        self._currency = currency
        self._shipping_address = shipping_address
        self._billing_address = billing_address
        super().__init__(id, created_at, updated_at)

    @property
    def user_id(self) -> Optional[EntityId]:
        return self._user_id

    @property
    def order_number(self) -> str:
        return self._order_number

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def total_amount(self) -> Decimal:
        return self._total_amount

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def shipping_address(self) -> Optional[dict]:
        return self._shipping_address

    @property
    def billing_address(self) -> Optional[dict]:
        return self._billing_address

    @classmethod
    def create(
        cls,
        user_id: Optional[EntityId],
        order_number: str,
        status: OrderStatus,
        total_amount: Decimal,
        currency: str,
        shipping_address: Optional[dict],
        billing_address: Optional[dict],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "OrderEntity":
        return cls(
            id=EntityId.generate(),
            user_id=user_id,
            order_number=order_number,
            status=status,
            total_amount=total_amount,
            currency=currency,
            shipping_address=shipping_address,
            billing_address=billing_address,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        user_id: Optional[EntityId] = None,
        status: Optional[OrderStatus] = None,
        total_amount: Optional[Decimal] = None,
        currency: Optional[str] = None,
        shipping_address: Optional[dict] = None,
        billing_address: Optional[dict] = None,
    ) -> None:
        if user_id is not None:
            self._user_id = user_id
        if status is not None:
            self._status = status
        if total_amount is not None:
            self._total_amount = total_amount
        if currency is not None:
            self._currency = currency
        if shipping_address is not None:
            self._shipping_address = shipping_address
        if billing_address is not None:
            self._billing_address = billing_address
        self.mark_as_updated()
