from dataclasses import dataclass

import bcrypt

# Configurable cost factor (12 is a good balance of security and performance)
_BCRYPT_ROUNDS = 12
# Bcrypt maximum password length in bytes
_MAX_PASSWORD_BYTES = 72
# Application minimum password length in characters
_MIN_PASSWORD_LENGTH = 8
# Application maximum password length in characters
_MAX_PASSWORD_LENGTH = 16


@dataclass(frozen=True)
class HashedPassword:
    """
    Value object representing a hashed password.
    Never stores plain text passwords.
    Uses bcrypt for secure hashing.
    """
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Hashed password cannot be empty")
        if not self._is_valid_hash(self.value):
            raise ValueError("Invalid password hash format")

    @staticmethod
    def _is_valid_hash(hashed: str) -> bool:
        """
        Validates that the string looks like a bcrypt hash.
        Bcrypt hashes start with $2a$, $2b$, or $2y$ and are 59-60 characters.
        """
        if not hashed:
            return False
        valid_prefixes = ("$2a$", "$2b$", "$2y$")
        return hashed.startswith(valid_prefixes) and 59 <= len(hashed) <= 60

    @classmethod
    def from_plain_text(cls, plain_password: str) -> "HashedPassword":
        """
        Factory method to create a HashedPassword from plain text.
        Hashes the password using bcrypt.

        Args:
            plain_password: The plain text password to hash.

        Returns:
            HashedPassword: A new instance with the hashed password.

        Raises:
            ValueError: If the plain password is empty or too short.
        """
        if not plain_password:
            raise ValueError("Password cannot be empty")
        if len(plain_password) < _MIN_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at least {_MIN_PASSWORD_LENGTH} characters long")
        if len(plain_password) > _MAX_PASSWORD_LENGTH:
            raise ValueError(f"Password cannot exceed {_MAX_PASSWORD_LENGTH} characters")

        password_bytes = plain_password.encode("utf-8")
        if len(password_bytes) > _MAX_PASSWORD_BYTES:
            raise ValueError(f"Password cannot exceed {_MAX_PASSWORD_BYTES} bytes")

        salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)

        return cls(value=hashed.decode("utf-8"))

    def verify(self, plain_password: str) -> bool:
        """
        Verifies a plain text password against this hashed password.

        Args:
            plain_password: The plain text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = self.value.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def __str__(self) -> str:
        """Returns a masked representation for security."""
        return "********"

    def __repr__(self) -> str:
        """Returns a masked representation for security."""
        return "HashedPassword(********)"

