from uuid import UUID

from src.app.features.band.application.dtos.band_dto import BandResponse
from src.app.features.band.application.mappers.band_mapper import to_band_response
from src.app.features.band.domain.exceptions.band_exception import BandDoesNotExistException
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class GetBandByIdUseCase:
    def __init__(self, band_repository: BandRepository):
        self.band_repository = band_repository

    async def execute(self, band_id: str) -> BandResponse:
        try:
            band_uuid = UUID(band_id)

            existing_band = await self.band_repository.find_by_id(band_uuid)

            if not existing_band:
                log.warning(f"Band not found with ID: {band_id}")
                raise BandDoesNotExistException(EntityId(band_uuid))

            return to_band_response(existing_band)

        except ValueError as e:
            log.error(f"Invalid UUID format for band ID {band_id}: {e}")
            raise ValueError(f"Invalid band ID format: {band_id}")
        except BandDoesNotExistException:
            log.error(f"Band does not exist with ID: {band_id}")
            raise
        except Exception as e:
            log.error(f"Unexpected error during get band by ID for {band_id}: {str(e)}")
            raise
