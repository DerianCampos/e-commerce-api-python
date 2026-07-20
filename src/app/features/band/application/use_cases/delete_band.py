from uuid import UUID

from src.app.features.band.domain.exceptions.band_exception import BandDoesNotExistException
from src.app.features.band.domain.repositories.band_repository import BandRepository
from src.app.shared.domain.value_objects.entity_id import EntityId
from src.app.shared.utils.log_util import log


class DeleteBandUseCase:
    def __init__(self, band_repository: BandRepository):
        self.band_repository = band_repository

    async def execute(self, band_id: str) -> bool:

        try:
            band_uuid = UUID(band_id)
            band_entity_id = EntityId(band_uuid)

            band_exists = await self.band_repository.exists(band_uuid)

            if not band_exists:
                log.warning(f"Cannot delete band. Band not found with ID: {band_id}")
                raise BandDoesNotExistException(band_entity_id)

            deleted = await self.band_repository.delete(band_uuid)

            if deleted:
                log.info(f"Band with ID {band_id} successfully deleted.")

            return deleted

        except ValueError as e:
            log.error(f"Invalid UUID format for band ID {band_id}: {e}")
            raise ValueError(f"Invalid band ID format: {band_id}")
        except BandDoesNotExistException:
            raise
        except Exception as e:
            log.error(f"Unexpected error during delete band for {band_id}: {str(e)}")
            raise
