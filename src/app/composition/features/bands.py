from fastapi import Depends

from src.app.composition.repositories import get_band_repository
from src.app.features.band.application.use_cases.create_band import CreateBandUseCase
from src.app.features.band.application.use_cases.delete_band import DeleteBandUseCase
from src.app.features.band.application.use_cases.get_band_by_id import GetBandByIdUseCase
from src.app.features.band.application.use_cases.list_bands import ListBandsUseCase
from src.app.features.band.application.use_cases.update_band import UpdateBandUseCase
from src.app.features.band.infrastructure.repository.band_repository_impl import BandRepositoryImpl


async def get_create_band_use_case(
    repo: BandRepositoryImpl = Depends(get_band_repository),
) -> CreateBandUseCase:
    return CreateBandUseCase(repo)


async def get_get_band_by_id_use_case(
    repo: BandRepositoryImpl = Depends(get_band_repository),
) -> GetBandByIdUseCase:
    return GetBandByIdUseCase(repo)


async def get_update_band_use_case(
    repo: BandRepositoryImpl = Depends(get_band_repository),
) -> UpdateBandUseCase:
    return UpdateBandUseCase(repo)


async def get_delete_band_use_case(
    repo: BandRepositoryImpl = Depends(get_band_repository),
) -> DeleteBandUseCase:
    return DeleteBandUseCase(repo)


async def get_list_bands_use_case(
    repo: BandRepositoryImpl = Depends(get_band_repository),
) -> ListBandsUseCase:
    return ListBandsUseCase(repo)
