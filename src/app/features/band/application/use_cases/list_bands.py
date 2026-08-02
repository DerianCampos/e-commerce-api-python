from typing import List, Optional

from src.app.features.band.application.dtos.band_dto import BandResponse
from src.app.features.band.application.mappers.band_mapper import to_band_response
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.shared.utils.log_util import log


class ListBandsUseCase:
    def __init__(self, band_repository: BandRepository):
        self.band_repository = band_repository

    async def execute(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[BandResponse]:
        try:
            bands = await self.band_repository.find_all(limit=limit, offset=offset)

            log.info(f"Listed {len(bands)} bands.")

            return [to_band_response(band) for band in bands]

        except Exception as e:
            log.error(f"Unexpected error during list bands: {str(e)}")
            raise
