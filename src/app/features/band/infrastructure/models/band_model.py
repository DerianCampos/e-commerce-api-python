from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class BandModel(BaseModel):
    __tablename__ = "bands"

    name = Column(String(150), unique=True, nullable=False)
    country = Column(String(100), nullable=True)
    genre = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    products = relationship("ProductModel", back_populates="band")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
