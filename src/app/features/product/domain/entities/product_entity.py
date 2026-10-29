from datetime import datetime
from typing import Optional

from src.app.features.product.domain.value_objects.fit import Fit
from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        name: str,
        description: Optional[str],
        fit: Fit,
        band_id: Optional[EntityId],
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._name = name
        self._description = description
        self._fit = fit
        self._band_id = band_id
        self._is_active = is_active
        super().__init__(id, created_at, updated_at)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def fit(self) -> Fit:
        return self._fit

    @property
    def band_id(self) -> Optional[EntityId]:
        return self._band_id

    @property
    def is_active(self) -> bool:
        return self._is_active

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str],
        fit: Fit,
        band_id: Optional[EntityId],
        is_active: bool,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "ProductEntity":
        return cls(
            id=EntityId.generate(),
            name=name,
            description=description,
            fit=fit,
            band_id=band_id,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        fit: Optional[Fit] = None,
        band_id: Optional[EntityId] = None,
        is_active: Optional[bool] = None,
    ) -> None:
        if name is not None:
            self._name = name
        if description is not None:
            self._description = description
        if fit is not None:
            self._fit = fit
        if band_id is not None:
            self._band_id = band_id
        if is_active is not None:
            self._is_active = is_active
        self.mark_as_updated()
