from src.app.shared.domain.value_objects.entity_id import EntityId


class BandDoesNotExistException(Exception):
    def __init__(self, band_id: EntityId):
        self.band_id = band_id
        super().__init__(f"Band with ID {band_id.value} does not exist.")
