import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import DeviceRepository, ReadingRepository, UserRepository
from app.schemas import ReadingCreate, ReadingResponse, ReadingResponseList


class ReadingService:
    def __init__(self, session: AsyncSession):
        self.reading_repo = ReadingRepository(session)
        self.device_repo = DeviceRepository(session)
        self.user_repo = UserRepository(session)

    async def create_reading(self, device_id: uuid.UUID, reading_data: ReadingCreate) -> ReadingResponse:
        try:
            device = await self.device_repo.get_device(device_id=device_id)
            if not device:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id = {device_id} not found"
                )

            reading = await self.reading_repo.create_reading(
                device_id=device_id, x=reading_data.x, y=reading_data.y, z=reading_data.z
            )

            await self.device_repo.update_last_reading_time(device_id=device_id)

            return reading

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e

    async def get_device_readings(
        self,
        device_id: uuid.UUID,
        from_date: datetime.datetime | None = None,
        to_date: datetime.datetime | None = None,
        limit: int = 1000,
    ) -> ReadingResponseList:
        try:
            device = await self.device_repo.get_device(device_id=device_id)
            if not device:
                raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

            await self.user_repo.update_last_used(user_id=device.user_id)
            return await self.reading_repo.get_device_readings(
                device_id=device_id, from_date=from_date, to_date=to_date, limit=limit
            )

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e
