import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.logging.config import logger
from app.schemas import ReadingCreate, ReadingResponse, ReadingResponseList
from app.services import ReadingService

reading_router = APIRouter(
    prefix="/reading",
    tags=["reading"],
)


@reading_router.post("/{device_id}", response_model=ReadingResponse, status_code=status.HTTP_201_CREATED)
async def create_reading(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    device_id: uuid.UUID,
    request: ReadingCreate,
):
    logger.debug(f"(router) Creating reading for device {device_id}")
    try:
        service = ReadingService(session)
        reading = await service.create_reading(device_id, request)
        logger.debug(f"(router) Created reading for device {device_id}")
        return reading

    except HTTPException as e:
        if e.status_code == 404:
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
            f"(router) Failed to create reading"
            f" with x = {request.x}, y = {request.y}, z = {request.z} and device_id = {device_id}",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise


@reading_router.get("/{device_id}", response_model=ReadingResponseList)
async def get_device_readings(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    device_id: uuid.UUID,
    from_date: datetime.datetime | None = None,
    to_date: datetime.datetime | None = None,
    limit: Annotated[int, Query(ge=1, le=1000)] = 50,
):
    logger.debug(f"(router) Getting readings for device {device_id}")
    try:
        service = ReadingService(session)
        result = await service.get_device_readings(device_id, from_date, to_date, limit)
        logger.debug(f"(router) Found {result.count} readings")
        return result

    except HTTPException as e:
        if e.status_code == 404:
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
            "(router) Failed to get device readings",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise
