from dataclasses import dataclass

from passlib.context import CryptContext

# Bcrypt context for hashing and verifying passwords
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class HashedPassword:
    """
    Value object representing a hashed password.
    Never stores plain text passwords.
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
        Bcrypt hashes start with $2a$, $2b$, or $2y$ and are 60 characters.
        """
        if not hashed:
            return False
        valid_prefixes = ("$2a$", "$2b$", "$2y$")
        return hashed.startswith(valid_prefixes) and len(hashed) == 60

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
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        hashed = _pwd_context.hash(plain_password)
        return cls(value=hashed)

    def verify(self, plain_password: str) -> bool:
        """
        Verifies a plain text password against this hashed password.

        Args:
            plain_password: The plain text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return _pwd_context.verify(plain_password, self.value)

    def __str__(self) -> str:
        """Returns a masked representation for security."""
        return "********"

    def __repr__(self) -> str:
        """Returns a masked representation for security."""
        return "HashedPassword(********)"

