from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.bands import (
    get_create_band_use_case,
    get_delete_band_use_case,
    get_get_band_by_id_use_case,
    get_list_bands_use_case,
    get_update_band_use_case,
)
from src.app.features.band.application.dtos.band_dto import (
    BandCreateRequest,
    BandResponse,
    BandUpdateRequest,
)
from src.app.features.band.application.use_cases.create_band import CreateBandUseCase
from src.app.features.band.application.use_cases.delete_band import DeleteBandUseCase
from src.app.features.band.application.use_cases.get_band_by_id import GetBandByIdUseCase
from src.app.features.band.application.use_cases.list_bands import ListBandsUseCase
from src.app.features.band.application.use_cases.update_band import UpdateBandUseCase
from src.app.features.band.domain.exceptions.band_exception import BandDoesNotExistException

router = APIRouter()


@router.get("/", response_model=List[BandResponse], status_code=status.HTTP_200_OK)
async def list_bands(
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    use_case: ListBandsUseCase = Depends(get_list_bands_use_case),
) -> List[BandResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{band_id}", response_model=BandResponse, status_code=status.HTTP_200_OK)
async def get_band_by_id(
    band_id: str,
    use_case: GetBandByIdUseCase = Depends(get_get_band_by_id_use_case),
) -> BandResponse:
    try:
        return await use_case.execute(band_id)
    except BandDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=BandResponse, status_code=status.HTTP_201_CREATED)
async def create_band(
    payload: BandCreateRequest,
    use_case: CreateBandUseCase = Depends(get_create_band_use_case),
) -> BandResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A band with this name already exists."
        )
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{band_id}", response_model=BandResponse, status_code=status.HTTP_200_OK)
async def update_band(
    band_id: str,
    payload: BandUpdateRequest,
    use_case: UpdateBandUseCase = Depends(get_update_band_use_case),
) -> BandResponse:
    try:
        return await use_case.execute(band_id, payload)
    except BandDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{band_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_band(
    band_id: str,
    use_case: DeleteBandUseCase = Depends(get_delete_band_use_case),
) -> None:
    try:
        await use_case.execute(band_id)
    except BandDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
