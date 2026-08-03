from src.app.shared.domain.value_objects.entity_id import EntityId


class ProductDoesNotExistException(Exception):
    """
    Exception raised when a product does not exist in the system.
    """

    def __init__(self, product_id: EntityId):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id.value} does not exist.")
