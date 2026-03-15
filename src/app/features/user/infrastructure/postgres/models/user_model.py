from sqlalchemy import Column, String, Boolean
from src.shared.infrastructure.postgres.models.base_model import BaseModel


class UserModel(BaseModel):
    """
    SQLAlchemy model for the 'users' table.
    Inherits common fields from BaseModel.
    """

    __tablename__ = 'users'


    # Additional fields specific to the UserModel can be defined here
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(8), nullable=False)
    is_active = Column(Boolean)
