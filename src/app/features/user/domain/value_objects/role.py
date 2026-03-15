from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

    @classmethod
    def from_str(cls, s: str) -> "Role":
        if not isinstance(s, str):
            raise TypeError(f"Role must be a string, got {type(s).__name__}")
        normalized = s.strip().casefold()
        try:
            return cls(normalized)
        except ValueError:
            valid = ", ".join(m.value for m in cls)
            raise ValueError(f"Invalid role: '{s}'. Valid roles are: {valid}")

    def __str__(self) -> str:
        return self.value

    @property
    def is_admin(self) -> bool:
        return self is Role.ADMIN

    @property
    def is_user(self) -> bool:
        return self is Role.USER