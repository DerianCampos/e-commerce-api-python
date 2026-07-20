from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class ProductModel(BaseModel):
    """
    SQLAlchemy model for the 'products' table.
    Inherits common fields from BaseModel.
    """

    __tablename__ = "products"

    band_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    fit = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
