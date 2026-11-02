from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class ProductVariantModel(BaseModel):
    __tablename__ = "product_variants"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    size_id = Column(
        UUID(as_uuid=True), ForeignKey("t_shirt_sizes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    color = Column(String(50), nullable=False, default="black")
    sku = Column(String(50), unique=True, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("product_id", "size_id", "color", name="uq_product_variants_product_size_color"),
    )

    product = relationship("ProductModel", back_populates="variants")
    size = relationship("TShirtSizeModel")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
