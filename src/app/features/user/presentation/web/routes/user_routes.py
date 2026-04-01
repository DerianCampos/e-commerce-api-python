from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends

from src.app.features.user.application.dtos.user_dto import UserResponse, UserCreate, UserUpdate
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)) -> None:
    """
    Delete a user by their ID.

    Args:
        user_id (UUID): The user's unique identifier.

    Returns:
        None: Returns 204 No Content on success.
    """
    await user_service.delete_user(str(user_id))


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Partially update a user by their ID.

    Args:
        user_id (UUID): The user's unique identifier.
        user_update (UserUpdate): The fields to update.

    Returns:
        UserResponse: The updated user's details.
    """
    return await user_service.update_user(str(user_id), user_update)

