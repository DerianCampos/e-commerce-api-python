from datetime import datetime
from typing import Optional

from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.domain.value_objects.role import Role
from src.shared.domain.entities.base_entity import BaseEntity
from src.shared.domain.value_objects.entity_id import EntityId


class UserEntity(BaseEntity):

    def __init__(self, id: EntityId, email: Email, first_name: str, last_name: str, role: Role, is_active: bool,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.is_active = is_active
        super().__init__(id, created_at, updated_at)
