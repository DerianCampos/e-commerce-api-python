from fastapi import Depends

from src.app.composition.repositories import get_user_repository

from src.app.features.user.application.use_cases.create_user import CreateUserUseCase
from src.app.features.user.application.use_cases.delete_user import DeleteUserUseCase
from src.app.features.user.application.use_cases.get_user_by_id import GetUserByIdUseCase
from src.app.features.user.application.use_cases.update_user import UpdateUserUseCase

from src.app.features.user.infrastructure.repository.user_repository_impl import UserRepositoryImpl


async def get_create_user_use_case(
        repo: UserRepositoryImpl = Depends(get_user_repository)
        ) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


async def get_get_user_by_id_use_case(
        repo: UserRepositoryImpl = Depends(get_user_repository)
        ) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)


async def get_update_user_use_case(
        repo: UserRepositoryImpl = Depends(get_user_repository)
        ) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


async def get_delete_user_use_case(
        repo: UserRepositoryImpl = Depends(get_user_repository)
        ) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)