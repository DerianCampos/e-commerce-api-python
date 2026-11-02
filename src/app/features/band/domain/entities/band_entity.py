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
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._name = name
        self._country = country
        self._genre = genre
        self._description = description
        self._image_url = image_url
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

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def image_url(self) -> Optional[str]:
        return self._image_url

    @classmethod
    def create(
        cls,
        name: str,
        country: Optional[str],
        genre: Optional[str],
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "BandEntity":
        return cls(
            id=EntityId.generate(),
            name=name,
            country=country,
            genre=genre,
            description=description,
            image_url=image_url,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        name: Optional[str] = None,
        country: Optional[str] = None,
        genre: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> None:
        if name is not None:
            self._name = name
        if country is not None:
            self._country = country
        if genre is not None:
            self._genre = genre
        if description is not None:
            self._description = description
        if image_url is not None:
            self._image_url = image_url
        self.mark_as_updated()
