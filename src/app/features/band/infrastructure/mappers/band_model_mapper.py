from src.app.features.band.domain.entities.band_entity import BandEntity
from src.app.shared.domain.value_objects.entity_id import EntityId


class BandModelMapper:
    @staticmethod
    def to_band_model(band_entity):
        return {
            "id": str(band_entity.id.value),
            "name": band_entity.name,
            "country": band_entity.country,
            "genre": band_entity.genre,
            "created_at": band_entity.created_at,
            "updated_at": band_entity.updated_at,
        }

    @staticmethod
    def to_band_entity(band_model):
        if band_model is None:
            return None
        return BandEntity(
            id=EntityId(band_model.id),
            name=band_model.name,
            country=band_model.country,
            genre=band_model.genre,
            created_at=band_model.created_at,
            updated_at=band_model.updated_at,
        )
