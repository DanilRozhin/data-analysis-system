import datetime
import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import DeviceRepository, ReadingRepository
from app.schemas import ReadingCreate, ReadingResponse


class ReadingService:
    def __init__(self, session: AsyncSession):
        self.reading_repo = ReadingRepository(session)
        self.device_repo = DeviceRepository(session)

    async def create_reading(self, device_id: uuid.UUID, reading_data: ReadingCreate) -> ReadingResponse:
        try:
            device = await self.device_repo.get_device(device_id=device_id)
            if not device:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device {device_id} not found")

            return await self.reading_repo.create_reading(
                device_id=device_id, x=reading_data.x, y=reading_data.y, z=reading_data.z
            )

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
    ) -> list[ReadingResponse]:
        device = await self.device_repo.get_device(device_id=device_id)
        if not device:
            raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

        return await self.reading_repo.get_device_readings(
            device_id=device_id, from_date=from_date, to_date=to_date, limit=limit
        )
