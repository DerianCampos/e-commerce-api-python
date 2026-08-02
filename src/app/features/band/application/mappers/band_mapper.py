from typing import Union

from pydantic import BaseModel

from src.app.features.band.application.dtos.band_dto import BandCreateRequest, BandResponse
from src.app.features.band.domain.entities.band_entity import BandEntity


def to_band_response(band_entity: Union[BaseModel, BandEntity]) -> BandResponse:
    return BandResponse(
        id=str(band_entity.id.value),
        name=band_entity.name,
        country=band_entity.country,
        genre=band_entity.genre,
    )


def to_band_entity(band_dto: BandCreateRequest) -> BandEntity:
    return BandEntity.create(
        name=band_dto.name,
        country=band_dto.country,
        genre=band_dto.genre,
    )
