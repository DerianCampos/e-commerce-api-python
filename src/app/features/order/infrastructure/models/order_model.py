from sqlalchemy import JSON, Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class OrderModel(BaseModel):
    """
    SQLAlchemy model for the 'orders' table.
    Inherits common fields from BaseModel.
    """

    __tablename__ = "orders"

    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    order_number = Column(String(30), unique=True, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="pending")
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="USD")
    shipping_address = Column(JSON, nullable=True)
    billing_address = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
