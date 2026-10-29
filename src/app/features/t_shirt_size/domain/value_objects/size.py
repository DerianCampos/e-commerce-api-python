from enum import Enum


class Size(Enum):
    XXS = "XXS"
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"

    @classmethod
    def from_str(cls, value: str) -> "Size":
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(f"Invalid size value: {value}. Allowed: {', '.join(s.value for s in cls)}")

    def __str__(self) -> str:
        return self.value
