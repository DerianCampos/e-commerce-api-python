from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductVariantDoesNotExistException(Exception):
    def __init__(self, variant_id: EntityId):
        self.variant_id = variant_id
        super().__init__(f"Product variant with ID {variant_id.value} does not exist.")
