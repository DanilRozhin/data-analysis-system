import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.logging.config import logger
from app.schemas import StatsResponse, UserAggregatedStatsResponse
from app.services import StatsService

stats_router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)


@stats_router.get("/device/{device_id}", response_model=StatsResponse)
async def get_device_stats(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    device_id: uuid.UUID,
    from_date: datetime.datetime | None = None,
    to_date: datetime.datetime | None = None,
):
    logger.debug(f"(router) Getting stats for device {device_id}")
    try:
        service = StatsService(session)
        stats = await service.get_device_stats(device_id, from_date, to_date)
        logger.debug(f"(router) Returned stats with device_id = {device_id}")
        return stats

    except HTTPException as e:
        if e.status_code == 404:
            logger.warning(
                f"Failed to get device stats with device_uuid = {device_id}, device not found",
                exc_info=False,
                extra={
                    "error_message": "Not found",
                },
            )
        raise

    except Exception as e:
        logger.error(
            "(router) Failed to get device stats",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise


@stats_router.get("/user/{user_id}/aggregated", response_model=UserAggregatedStatsResponse)
async def get_user_aggregated_stats(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_id: uuid.UUID,
    from_date: datetime.datetime | None = None,
    to_date: datetime.datetime | None = None,
):
    logger.debug(f"(router) Getting aggregated stats for user {user_id}")
    try:
        service = StatsService(session)
        user_stats = await service.get_user_aggregated_stats(user_id, from_date, to_date)
        logger.debug(f"(router) Returned stats with user_id = {user_id}")
        return user_stats

    except HTTPException as e:
        if e.status_code == 404:
            logger.warning(
                f"Failed to get aggregated stats for user with uuid: {user_id}, user not found",
                exc_info=False,
                extra={
                    "error_message": "Not found",
                },
            )
        raise

    except Exception as e:
        logger.error(
            "(router) Failed to get aggregated stats",
            exc_info=True,
            extra={
                "error_message": str(e),
            },
        )
        raise
