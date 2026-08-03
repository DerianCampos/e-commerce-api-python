import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Sku:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("SKU must be a non-empty string")
        if len(self.value) > 50:
            raise ValueError("SKU must not exceed 50 characters")
        if not re.match(r"^[A-Z0-9\-]+$", self.value):
            raise ValueError("SKU must contain only uppercase letters, digits, and hyphens")

    def __str__(self) -> str:
        return self.value
