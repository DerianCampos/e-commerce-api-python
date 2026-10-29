from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderDoesNotExistException(Exception):
    """
    Exception raised when an order does not exist in the system.
    """

    def __init__(self, order_id: EntityId):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id.value} does not exist.")
