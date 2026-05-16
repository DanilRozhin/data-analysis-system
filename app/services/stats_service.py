import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import DeviceRepository, ReadingRepository, UserRepository
from app.schemas import DeviceStatsResponse, StatsResponse, UserAggregatedStatsResponse


def _calculate_statistics(
    values: list[float],
    readings_count: int,
    period_from: datetime.datetime | None = None,
    period_to: datetime.datetime | None = None,
) -> StatsResponse:
    if not values:
        return StatsResponse(
            min_value=None,
            max_value=None,
            readings_amount=0,
            sum_value=None,
            median=None,
            period_to=period_to,
            period_from=period_from,
        )

    sorted_values = sorted(values)
    n = len(sorted_values)

    if n % 2 == 0:
        median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        median = sorted_values[n // 2]

    return StatsResponse(
        min_value=float(min(values)),
        max_value=float(max(values)),
        readings_amount=readings_count,
        sum_value=float(sum(values)),
        median=float(median),
        period_to=period_to,
        period_from=period_from,
    )


class StatsService:
    def __init__(self, session: AsyncSession):
        self.device_repo = DeviceRepository(session)
        self.user_repo = UserRepository(session)
        self.reading_repo = ReadingRepository(session)

    async def get_device_stats(
        self,
        device_id: uuid.UUID,
        period_from: datetime.datetime | None = None,
        period_to: datetime.datetime | None = None,
    ) -> StatsResponse:
        try:
            device = await self.device_repo.get_device(device_id)
            if not device:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id = {device_id} not found"
                )

            await self.user_repo.update_last_used(user_id=device.user_id)

            result = await self.reading_repo.get_device_readings(device_id, period_from, period_to)
            readings = result.readings
            values = []
            for r in readings:
                values.extend([r.x, r.y, r.z])
            stats = _calculate_statistics(
                values=values,
                period_from=period_from,
                period_to=period_to,
                readings_count=len(readings),
            )
            return stats

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e

    async def get_user_aggregated_stats(
        self,
        user_id: uuid.UUID,
        period_from: datetime.datetime | None = None,
        period_to: datetime.datetime | None = None,
    ) -> UserAggregatedStatsResponse:
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")

            devices = await self.device_repo.get_user_devices(user_id=user_id)

            if not devices:
                return UserAggregatedStatsResponse(
                    user_id=user_id,
                    total_devices=0,
                    total_readings=0,
                    statistics=None,
                    devices_stats=[],
                )

            devices_stats = []
            all_values = []
            total_readings = 0

            for device in devices:
                result = await self.reading_repo.get_device_readings(device.id, period_from, period_to)
                readings = result.readings
                total_readings += len(readings)

                values = []
                for r in readings:
                    values.extend([r.x, r.y, r.z])

                device_stats = _calculate_statistics(
                    values=values,
                    period_from=period_from,
                    period_to=period_to,
                    readings_count=len(readings),
                )

                devices_stats.append(
                    DeviceStatsResponse(
                        device_id=device.id,
                        device_name=device.name,
                        statistics=device_stats,
                    )
                )

                all_values.extend(values)

            total_stats = (
                _calculate_statistics(
                    values=all_values,
                    period_from=period_from,
                    period_to=period_to,
                    readings_count=total_readings,
                )
                if all_values
                else None
            )

            return UserAggregatedStatsResponse(
                user_id=user_id,
                total_devices=len(devices),
                total_readings=total_readings,
                statistics=total_stats,
                devices_stats=devices_stats,
            )

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e
