from typing import Union

from pydantic import BaseModel

from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import TShirtSizeCreateRequest, TShirtSizeResponse
from src.app.features.t_shirt_size.domain.entities.t_shirt_size_entity import TShirtSizeEntity
from src.app.features.t_shirt_size.domain.value_objects.size import Size


def to_t_shirt_size_response(size_entity: Union[BaseModel, TShirtSizeEntity]) -> TShirtSizeResponse:
    return TShirtSizeResponse(
        id=str(size_entity.id.value),
        size=str(size_entity.size),
        chest_min_cm=size_entity.chest_min_cm,
        chest_max_cm=size_entity.chest_max_cm,
    )


def to_t_shirt_size_entity(size_dto: TShirtSizeCreateRequest) -> TShirtSizeEntity:
    return TShirtSizeEntity.create(
        size=Size.from_str(size_dto.size),
        chest_min_cm=size_dto.chest_min_cm,
        chest_max_cm=size_dto.chest_max_cm,
    )
