from datetime import datetime
from typing import Optional

from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class BandEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        name: str,
        country: Optional[str],
        genre: Optional[str],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._name = name
        self._country = country
        self._genre = genre
        super().__init__(id, created_at, updated_at)

    @property
    def name(self) -> str:
        return self._name

    @property
    def country(self) -> Optional[str]:
        return self._country

    @property
    def genre(self) -> Optional[str]:
        return self._genre

    @classmethod
    def create(
        cls,
        name: str,
        country: Optional[str],
        genre: Optional[str],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "BandEntity":
        return cls(
            id=EntityId.generate(),
            name=name,
            country=country,
            genre=genre,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        name: Optional[str] = None,
        country: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> None:
        if name is not None:
            self._name = name
        if country is not None:
            self._country = country
        if genre is not None:
            self._genre = genre
        self.mark_as_updated()
