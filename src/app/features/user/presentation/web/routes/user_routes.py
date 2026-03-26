from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends

from src.app.features.user.application.dtos.user_dto import UserResponse, UserCreate
from src.app.features.user.application.services.user_service import UserService
from src.app.features.user.presentation.web.dependencies import get_user_service

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: UUID, user_service: UserService = Depends(get_user_service)) -> UserResponse:
    # """
    # Get a user by their ID.
    #
    # Args:
    #     user_id (UUID): The user's unique identifier.
    #
    # Returns:
    #     UserResponse: The user's details.
    # """
    user_result = await user_service.get_user_by_id(str(user_id))

    return user_result

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, user_service: UserService = Depends(get_user_service)) -> UserResponse:
    # """
    # Create a new user.
    #
    # Returns:
    #     UserResponse: The created user's details.
    # """
    user_result = await user_service.save_user(user_create)

    return user_result