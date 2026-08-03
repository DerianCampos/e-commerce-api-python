from src.app.shared.domain.value_objects.entity_id import EntityId


class OrderItemDoesNotExistException(Exception):
    """
    Exception raised when an order item does not exist in the system.
    """

    def __init__(self, order_item_id: EntityId):
        self.order_item_id = order_item_id
        super().__init__(f"Order item with ID {order_item_id.value} does not exist.")
