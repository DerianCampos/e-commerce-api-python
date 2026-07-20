from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from src.app.shared.persistence.base_model import BaseModel


class BandModel(BaseModel):
    __tablename__ = "bands"

    name = Column(String(150), unique=True, nullable=False)
    country = Column(String(100), nullable=True)
    genre = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
