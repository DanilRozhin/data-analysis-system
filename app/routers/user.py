import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.logging.config import logger
from app.schemas import UserCreate, UserResponse
from app.services import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: uuid.UUID,
):
    logger.debug(f"(router) Getting user with uuid = {user_id}")
    try:
        user_service = UserService(session=session)
        user = await user_service.get_user(user_id=user_id)
        logger.debug(f"(router) Returned user with uuid = {user_id}")
        return user

    except HTTPException:
        logger.error(
            f"Failed to get user with uuid = {user_id}",
            exc_info=False,
            extra={
                "error_message": "Not found",
            },
        )
        raise

    except Exception as e:
        logger.error(
            f"Failed to get user with uuid = {user_id}",
            exc_info=False,
            extra={
                "error_message": str(e),
            },
        )
        raise


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    request: UserCreate,
):
    logger.debug(f"(router) Creating new user with name = {request.name}")
    try:
        user_service = UserService(session=session)
        user = await user_service.create_user(username=request.name)
        logger.debug(f"(router) Created user with name = {request.name} and uuid = {user.id}")
        return user

    except Exception as e:
        logger.error(
            f"(router) Failed to create user with name = {request.name}",
            exc_info=False,
            extra={
                "error_message": str(e),
            },
        )
        raise
