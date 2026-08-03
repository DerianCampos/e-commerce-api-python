from fastapi import Depends

from src.app.composition.repositories import get_t_shirt_size_repository
from src.app.features.t_shirt_size.application.use_cases.create_t_shirt_size import CreateTShirtSizeUseCase
from src.app.features.t_shirt_size.application.use_cases.delete_t_shirt_size import DeleteTShirtSizeUseCase
from src.app.features.t_shirt_size.application.use_cases.get_t_shirt_size_by_id import GetTShirtSizeByIdUseCase
from src.app.features.t_shirt_size.application.use_cases.list_t_shirt_sizes import ListTShirtSizesUseCase
from src.app.features.t_shirt_size.application.use_cases.update_t_shirt_size import UpdateTShirtSizeUseCase
from src.app.features.t_shirt_size.infrastructure.repository.t_shirt_size_repository_impl import (
    TShirtSizeRepositoryImpl,
)


async def get_create_t_shirt_size_use_case(
    repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> CreateTShirtSizeUseCase:
    return CreateTShirtSizeUseCase(repo)


async def get_get_t_shirt_size_by_id_use_case(
    repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> GetTShirtSizeByIdUseCase:
    return GetTShirtSizeByIdUseCase(repo)


async def get_update_t_shirt_size_use_case(
    repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> UpdateTShirtSizeUseCase:
    return UpdateTShirtSizeUseCase(repo)


async def get_delete_t_shirt_size_use_case(
    repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> DeleteTShirtSizeUseCase:
    return DeleteTShirtSizeUseCase(repo)


async def get_list_t_shirt_sizes_use_case(
    repo: TShirtSizeRepositoryImpl = Depends(get_t_shirt_size_repository),
) -> ListTShirtSizesUseCase:
    return ListTShirtSizesUseCase(repo)
