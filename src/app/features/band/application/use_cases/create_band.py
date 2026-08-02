from src.app.features.band.application.dtos.band_dto import BandCreateRequest, BandResponse
from src.app.features.band.application.mappers.band_mapper import to_band_entity, to_band_response
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.shared.logging.logging import get_logger

log = get_logger(__name__)

class CreateBandUseCase:
    def __init__(self, band_repository: BandRepository):
        self.band_repository = band_repository

    async def execute(self, payload: BandCreateRequest) -> BandResponse:
        try:
            band_entity = to_band_entity(payload)

            created_band = await self.band_repository.create(band_entity)
            log.info(f"Band created: {created_band.name}")

            return to_band_response(created_band)

        except Exception as e:
            log.error(f"Unexpected error while saving band: {str(e)}")
            raise
