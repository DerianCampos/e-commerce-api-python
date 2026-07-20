from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class TShirtSizeModel(BaseModel):
    __tablename__ = "t_shirt_sizes"

    size = Column(String(10), unique=True, nullable=False)
    chest_min_cm = Column(Integer, nullable=True)
    chest_max_cm = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
