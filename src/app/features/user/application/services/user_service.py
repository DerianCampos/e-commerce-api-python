from src.app.features.user.application.use_cases.get_user_by_id import GetUserByIdUseCase
from src.app.features.user.application.use_cases.save_user import SaveUser
from src.app.features.user.domain.repositories.user_repository import UserRepository
from src.app.features.user.application.dtos.user_dto import UserCreate, UserResponse


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str):
        use_case = GetUserByIdUseCase(self.user_repository)

        return await use_case.execute(user_id)
    
    async def save_user(self, user_create: UserCreate) -> UserResponse:
        use_case = SaveUser(self.user_repository)

        return await use_case.execute(user_create)
