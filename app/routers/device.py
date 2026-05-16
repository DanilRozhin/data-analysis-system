import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.logging.config import logger
from app.schemas import DeviceCreate, DeviceResponse, DeviceResponseList
from app.services import DeviceService

device_router = APIRouter(
    prefix="/device",
    tags=["device"],
)


@device_router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    device_id: uuid.UUID,
):
    logger.debug(f"(router) Getting device with uuid = {device_id}")
    try:
        device_service = DeviceService(session=session)
        device = await device_service.get_device(device_id=device_id)
        logger.debug(f"(router) Returned device with uuid = {device_id}")
        return device

    except HTTPException:
        logger.error(
            f"Failed to get device with uuid = {device_id}, device not found",
            exc_info=False,
            extra={
                "error_message": "Not found",
            },
        )
        raise

    except Exception as e:
        logger.error(
            f"Failed to get device with uuid = {device_id}",
            exc_info=False,
            extra={
                "error_message": str(e),
            },
        )
        raise


@device_router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    request: DeviceCreate,
):
    logger.debug(f"(router) Creating new device with name = {request.name} and user_id = {request.user_id}")
    try:
        device_service = DeviceService(session=session)
        device = await device_service.create_device(
            device_name=request.name, user_id=request.user_id, device_description=request.description
        )
        logger.debug(f"(router) Created device with name = {request.name} and user_id = {request.user_id}")
        return device

    except HTTPException as e:
        if e.status_code == 404:
            logger.error(
                f"Failed to get user with uuid = {request.user_id}, device not found",
                exc_info=False,
                extra={
                    "error_message": "Not found",
                },
            )
        raise

    except Exception as e:
        logger.error(
            f"(router) Failed to create device with name = {request.name} and user_id = {request.user_id}",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise


@device_router.get("/user/{user_id}/devices", response_model=DeviceResponseList)
async def get_user_devices(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: uuid.UUID,
):
    logger.debug(f"(router) Getting all user devices with user uuid = {user_id}")
    try:
        device_service = DeviceService(session=session)
        devices = await device_service.get_user_devices(user_id=user_id)
        logger.debug(f"(router) Returned all user devices with user uuid = {user_id}")
        return devices

    except HTTPException as e:
        if e.status_code == 404:
            logger.error(
                f"Failed to get all user devices with user uuid = {user_id}, user not found",
                exc_info=False,
                extra={
                    "error_message": str(e),
                },
            )
            raise

    except Exception as e:
        logger.error(
            f"Failed to get all user devices with user uuid = {user_id}",
            exc_info=False,
            extra={
                "error_message": str(e),
            },
        )
        raise
