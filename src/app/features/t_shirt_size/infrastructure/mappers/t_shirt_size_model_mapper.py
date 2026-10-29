from src.app.features.t_shirt_size.domain.entities.t_shirt_size_entity import TShirtSizeEntity
from src.app.features.t_shirt_size.domain.value_objects.size import Size
from src.app.shared.domain.value_objects.entity_id import EntityId


class TShirtSizeModelMapper:
    @staticmethod
    def to_t_shirt_size_model(size_entity):
        return {
            "id": str(size_entity.id.value),
            "size": str(size_entity.size),
            "chest_min_cm": size_entity.chest_min_cm,
            "chest_max_cm": size_entity.chest_max_cm,
            "created_at": size_entity.created_at,
            "updated_at": size_entity.updated_at,
        }

    @staticmethod
    def to_t_shirt_size_entity(size_model):
        if size_model is None:
            return None
        return TShirtSizeEntity(
            id=EntityId(size_model.id),
            size=Size.from_str(size_model.size),
            chest_min_cm=size_model.chest_min_cm,
            chest_max_cm=size_model.chest_max_cm,
            created_at=size_model.created_at,
            updated_at=size_model.updated_at,
        )
