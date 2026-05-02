from src.app.features.user.application.use_cases.delete_user import DeleteUserUseCase
from src.app.features.user.application.use_cases.get_user_by_id import GetUserByIdUseCase
from src.app.features.user.application.use_cases.save_user import SaveUser
from src.app.features.user.application.use_cases.update_user import UpdateUserUseCase
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.application.dtos.user_dto import UserCreate, UserResponse, UserUpdate


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        use_case = GetUserByIdUseCase(self.user_repository)

        return await use_case.execute(user_id)
    
    async def save_user(self, user_create: UserCreate) -> UserResponse:
        use_case = SaveUser(self.user_repository)

        return await use_case.execute(user_create)

    async def delete_user(self, user_id: str) -> bool:
        use_case = DeleteUserUseCase(self.user_repository)

        return await use_case.execute(user_id)

    async def update_user(self, user_id: str, user_update: UserUpdate) -> UserResponse:
        use_case = UpdateUserUseCase(self.user_repository)

        return await use_case.execute(user_id, user_update)

