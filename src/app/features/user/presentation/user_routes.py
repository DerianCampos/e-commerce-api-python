from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.users import get_create_user_use_case, get_get_user_by_id_use_case, get_update_user_use_case, get_delete_user_use_case

from src.app.features.user.application.dtos.user_dto import UserCreateRequest, UserResponse, UserUpdateRequest
from src.app.features.user.application.use_cases.create_user import CreateUserUseCase
from src.app.features.user.application.use_cases.delete_user import DeleteUserUseCase
from src.app.features.user.application.use_cases.get_user_by_id import GetUserByIdUseCase
from src.app.features.user.application.use_cases.update_user import UpdateUserUseCase
from src.app.features.user.domain.exceptions.user_exception import UserDoesNotExistException


router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: str,
    use_case: GetUserByIdUseCase = Depends(get_get_user_by_id_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id)
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists.")
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id, payload)
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
) -> None:
    try:
        await use_case.execute(user_id)
    except UserDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
