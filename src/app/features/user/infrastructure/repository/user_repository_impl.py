from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.features.user.domain.entities.user_entity import UserEntity
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.domain.value_objects.email import Email
from src.app.features.user.infrastructure.models.user_model import UserModel
from src.app.features.user.infrastructure.mappers.user_model_mapper import to_user_entity
from app.shared.domain.repositories.base_repository import ID, T
from app.shared.utils.log_util import log


class UserRepositoryImpl(UserRepository):

    def __init__(self, db_session: AsyncSession):
        """
        Initializes the UserRepositoryImpl with a SQLAlchemy AsyncSession.

        Args:
            db_session (AsyncSession): The SQLAlchemy session to use for database operations.
        """
        self.db_session = db_session

    async def find_by_id(self, entity_id: ID) -> Optional[UserEntity]:
        user_model: Optional[UserModel] = await self.db_session.get(UserModel, entity_id)

        return to_user_entity(user_model)

    async def find_by_email(self, email: Email) -> Optional[UserEntity]:
        stmt = select(UserModel).where(UserModel.email == email.value)

        result = await self.db_session.execute(stmt)

        user_model = result.scalar_one_or_none()

        if user_model is None:
            log.info(f"User with email {email.value} not found.")
            return None

        log.info(f"User with email {email.value} found.")
        return to_user_entity(user_model)

    async def find_by_name(self, record: str) -> Optional[UserEntity]:
        stmt = select(UserModel).where((UserModel.first_name == record) | (UserModel.last_name == record))
        result = await self.db_session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return to_user_entity(user_model)

    async def save(self, entity: T) -> T:
        """
        Persist a domain UserEntity into the database and return the saved entity.
        This method assumes `entity` is a `UserEntity` instance.
        """
        # Map domain entity to ORM model
        user_model = None
        try:
            # If the entity.id is an EntityId dataclass, it may contain a UUID object
            user_model = UserModel(
                id=entity.id.value if hasattr(entity.id, 'value') else entity.id,
                email=str(entity.email.value) if hasattr(entity.email, 'value') else str(entity.email),
                first_name=entity.first_name,
                last_name=entity.last_name,
                hashed_password=entity.hashed_password.value,
                role=str(entity.role.value) if hasattr(entity.role, 'value') else str(entity.role),
                is_active=bool(entity.is_active),
            )

            self.db_session.add(user_model)
            await self.db_session.commit()
            await self.db_session.refresh(user_model)

            return to_user_entity(user_model)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error saving user: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error saving user (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error saving user: {e}")
            raise

    async def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        stmt = select(UserModel)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db_session.execute(stmt)
        models = result.scalars().all()
        return [to_user_entity(m) for m in models]

    async def exists(self, entity_id: ID) -> bool:
        user_model = await self.db_session.get(UserModel, entity_id)
        return user_model is not None

    async def update(self, entity: T) -> Optional[T]:
        # Simple update: fetch by id then apply fields and commit
        existing = await self.db_session.get(UserModel, entity.id.value if hasattr(entity.id, 'value') else entity.id)
        if existing is None:
            return None

        existing.email = str(entity.email.value) if hasattr(entity.email, 'value') else str(entity.email)
        existing.first_name = entity.first_name
        existing.last_name = entity.last_name
        existing.hashed_password = entity.hashed_password.value
        existing.role = str(entity.role.value) if hasattr(entity.role, 'value') else str(entity.role)
        existing.is_active = bool(entity.is_active)

        try:
            self.db_session.add(existing)
            await self.db_session.commit()
            await self.db_session.refresh(existing)
            return to_user_entity(existing)

        except IntegrityError as ie:
            await self.db_session.rollback()
            log.error(f"Integrity error updating user: {ie}")
            raise
        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error updating user (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error updating user: {e}")
            raise

    async def delete(self, entity_id: ID) -> bool:
        existing = await self.db_session.get(UserModel, entity_id)
        if existing is None:
            return False

        try:
            await self.db_session.delete(existing)
            await self.db_session.commit()
            return True

        except OperationalError as e:
            await self.db_session.rollback()
            log.error(f"Operational error deleting user (connection/timeout issue): {e}")
            raise
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            log.error(f"Database error deleting user: {e}")
            raise
