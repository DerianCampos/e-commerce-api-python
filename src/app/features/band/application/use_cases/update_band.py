from uuid import UUID

from src.app.features.band.application.dtos.band_dto import BandResponse, BandUpdateRequest
from src.app.features.band.application.mappers.band_mapper import to_band_response
from src.app.features.band.domain.exceptions.band_exception import BandDoesNotExistException
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class UpdateBandUseCase:
    def __init__(self, band_repository: BandRepository):
        self.band_repository = band_repository

    async def execute(self, band_id: str, band_update: BandUpdateRequest) -> BandResponse:

        try:
            band_uuid = UUID(band_id)
            band_entity_id = EntityId(band_uuid)

            existing_band = await self.band_repository.find_by_id(band_uuid)

            if not existing_band:
                log.warning(f"Cannot update band. Band not found with ID: {band_id}")
                raise BandDoesNotExistException(band_entity_id)

            existing_band.update(
                name=band_update.name,
                country=band_update.country,
                genre=band_update.genre,
            )

            updated_band = await self.band_repository.update(existing_band)

            log.info(f"Band with ID {band_id} successfully updated.")

            return to_band_response(updated_band)

        except ValueError as e:
            log.error(f"Invalid UUID format for band ID {band_id}: {e}")
            raise ValueError(f"Invalid band ID format: {band_id}")
        except BandDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during update band for {band_id}: {str(e)}")
            raise
