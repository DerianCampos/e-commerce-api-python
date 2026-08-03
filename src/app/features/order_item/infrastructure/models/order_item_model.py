from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class OrderItemModel(BaseModel):
    """
    SQLAlchemy model for the 'order_items' table.
    Inherits common fields from BaseModel.
    """

    __tablename__ = "order_items"

    order_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_variant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_name = Column(String(150), nullable=False)
    band_name = Column(String(150), nullable=True)
    size = Column(String(10), nullable=False)
    color = Column(String(50), nullable=False)
    sku = Column(String(50), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    line_total = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
