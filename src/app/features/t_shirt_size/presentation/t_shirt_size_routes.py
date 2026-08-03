from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.t_shirt_sizes import (
    get_create_t_shirt_size_use_case,
    get_delete_t_shirt_size_use_case,
    get_get_t_shirt_size_by_id_use_case,
    get_list_t_shirt_sizes_use_case,
    get_update_t_shirt_size_use_case,
)
from src.app.features.t_shirt_size.application.dtos.t_shirt_size_dto import (
    TShirtSizeCreateRequest,
    TShirtSizeResponse,
    TShirtSizeUpdateRequest,
)
from src.app.features.t_shirt_size.application.use_cases.create_t_shirt_size import CreateTShirtSizeUseCase
from src.app.features.t_shirt_size.application.use_cases.delete_t_shirt_size import DeleteTShirtSizeUseCase
from src.app.features.t_shirt_size.application.use_cases.get_t_shirt_size_by_id import GetTShirtSizeByIdUseCase
from src.app.features.t_shirt_size.application.use_cases.list_t_shirt_sizes import ListTShirtSizesUseCase
from src.app.features.t_shirt_size.application.use_cases.update_t_shirt_size import UpdateTShirtSizeUseCase
from src.app.features.t_shirt_size.domain.exceptions.t_shirt_size_exception import TShirtSizeDoesNotExistException

router = APIRouter()


@router.get("/", response_model=List[TShirtSizeResponse], status_code=status.HTTP_200_OK)
async def list_t_shirt_sizes(
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    use_case: ListTShirtSizesUseCase = Depends(get_list_t_shirt_sizes_use_case),
) -> List[TShirtSizeResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{size_id}", response_model=TShirtSizeResponse, status_code=status.HTTP_200_OK)
async def get_t_shirt_size_by_id(
    size_id: str,
    use_case: GetTShirtSizeByIdUseCase = Depends(get_get_t_shirt_size_by_id_use_case),
) -> TShirtSizeResponse:
    try:
        return await use_case.execute(size_id)
    except TShirtSizeDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=TShirtSizeResponse, status_code=status.HTTP_201_CREATED)
async def create_t_shirt_size(
    payload: TShirtSizeCreateRequest,
    use_case: CreateTShirtSizeUseCase = Depends(get_create_t_shirt_size_use_case),
) -> TShirtSizeResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A t-shirt size with this size already exists."
        )
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{size_id}", response_model=TShirtSizeResponse, status_code=status.HTTP_200_OK)
async def update_t_shirt_size(
    size_id: str,
    payload: TShirtSizeUpdateRequest,
    use_case: UpdateTShirtSizeUseCase = Depends(get_update_t_shirt_size_use_case),
) -> TShirtSizeResponse:
    try:
        return await use_case.execute(size_id, payload)
    except TShirtSizeDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_t_shirt_size(
    size_id: str,
    use_case: DeleteTShirtSizeUseCase = Depends(get_delete_t_shirt_size_use_case),
) -> None:
    try:
        await use_case.execute(size_id)
    except TShirtSizeDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
