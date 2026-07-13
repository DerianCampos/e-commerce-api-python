

from app.shared.domain.value_objects.entity_id import EntityId


class UserDoesNotExistException(Exception):
    """
    Exception raised when a user does not exist in the system.
    """

    def __init__(self, user_id: EntityId):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id.value} does not exist.")