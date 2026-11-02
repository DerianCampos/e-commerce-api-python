import re
import unicodedata
from dataclasses import dataclass

_SKU_SANITIZE_PATTERN = re.compile(r"[^A-Za-z0-9]+")
_ASCII_REPLACEMENTS = str.maketrans(
    {
        "Æ": "AE",
        "æ": "ae",
        "Ø": "O",
        "ø": "o",
        "Ð": "D",
        "ð": "d",
        "Þ": "TH",
        "þ": "th",
        "ß": "SS",
        "Ł": "L",
        "ł": "l",
    }
)


def _slugify(value: str) -> str:
    """Normalize free text into uppercase ASCII words joined by hyphens."""
    translated = (value or "").translate(_ASCII_REPLACEMENTS)
    ascii_text = unicodedata.normalize("NFKD", translated).encode("ascii", "ignore").decode("ascii")
    return _SKU_SANITIZE_PATTERN.sub("-", ascii_text).strip("-").upper()


@dataclass(frozen=True)
class Sku:
    MAX_LENGTH = 50

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("SKU must be a non-empty string")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"SKU must not exceed {self.MAX_LENGTH} characters")
        if not re.match(r"^[A-Z0-9\-]+$", self.value):
            raise ValueError("SKU must contain only uppercase letters, digits, and hyphens")

    @classmethod
    def from_parts(cls, product_name: str, size: str, color: str = "") -> "Sku":
        """Build a readable SKU such as ``AENEMA-TOOL-L-BLACK`` from catalog data."""
        product_part = _slugify(product_name) or "PRODUCT"
        size_part = _slugify(size) or "OS"
        color_part = _slugify(color) or "DEFAULT"

        tail = f"-{size_part}-{color_part}"
        max_product_length = cls.MAX_LENGTH - len(tail)

        if max_product_length < 1:
            value = tail.strip("-")[: cls.MAX_LENGTH].strip("-")
        else:
            truncated_product = product_part[:max_product_length].strip("-")
            value = f"{truncated_product}{tail}"

        return cls(value)

    def __str__(self) -> str:
        return self.value
