from src.app.shared.domain.value_objects.entity_id import EntityId


class TShirtSizeDoesNotExistException(Exception):
    def __init__(self, size_id: EntityId):
        self.size_id = size_id
        super().__init__(f"T-shirt size with ID {size_id.value} does not exist.")
