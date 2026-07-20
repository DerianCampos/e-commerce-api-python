from datetime import datetime
from typing import Optional

from src.app.features.t_shirt_size.domain.value_objects.size import Size
from src.app.shared.domain.entities.base_entity import BaseEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class TShirtSizeEntity(BaseEntity):
    def __init__(
        self,
        id: EntityId,
        size: Size,
        chest_min_cm: Optional[int],
        chest_max_cm: Optional[int],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._size = size
        self._chest_min_cm = chest_min_cm
        self._chest_max_cm = chest_max_cm
        super().__init__(id, created_at, updated_at)

    @property
    def size(self) -> Size:
        return self._size

    @property
    def chest_min_cm(self) -> Optional[int]:
        return self._chest_min_cm

    @property
    def chest_max_cm(self) -> Optional[int]:
        return self._chest_max_cm

    @classmethod
    def create(
        cls,
        size: Size,
        chest_min_cm: Optional[int],
        chest_max_cm: Optional[int],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> "TShirtSizeEntity":
        return cls(
            id=EntityId.generate(),
            size=size,
            chest_min_cm=chest_min_cm,
            chest_max_cm=chest_max_cm,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        size: Optional[Size] = None,
        chest_min_cm: Optional[int] = None,
        chest_max_cm: Optional[int] = None,
    ) -> None:
        if size is not None:
            self._size = size
        if chest_min_cm is not None:
            self._chest_min_cm = chest_min_cm
        if chest_max_cm is not None:
            self._chest_max_cm = chest_max_cm
        self.mark_as_updated()
