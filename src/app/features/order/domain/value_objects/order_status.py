from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

    @classmethod
    def from_str(cls, value: str) -> "OrderStatus":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid order status value: {value}. Allowed: {', '.join(s.value for s in cls)}")

    def __str__(self) -> str:
        return self.value
