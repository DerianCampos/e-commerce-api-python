from enum import Enum


class Fit(Enum):
    UNISEX = "unisex"
    MEN = "men"
    WOMEN = "women"
    OVERSIZED = "oversized"

    @classmethod
    def from_str(cls, value: str) -> "Fit":
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid fit value: {value}. Allowed: {', '.join(f.value for f in cls)}")

    def __str__(self) -> str:
        return self.value
