import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Reading
from app.logging.config import logger
from app.schemas import ReadingResponse, ReadingResponseList


class ReadingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_reading(self, device_id: uuid.UUID, x: float, y: float, z: float) -> ReadingResponse:
        logs_extra = {
            "method": "create_reading",
            "service": "reading_repository",
            "device_id": str(device_id),
            "x": x,
            "y": y,
            "z": z,
        }

        reading = Reading(
            device_id=device_id,
            x=x,
            y=y,
            z=z,
        )

        logger.debug(f"(repository) Creating reading for device {device_id}", extra=logs_extra)

        self.session.add(reading)
        await self.session.commit()
        await self.session.refresh(reading)

        return ReadingResponse.model_validate(reading)

    async def get_device_readings(
        self,
        device_id: uuid.UUID,
        from_date: datetime.datetime | None = None,
        to_date: datetime.datetime | None = None,
        limit: int = 50,
    ) -> ReadingResponseList:
        logs_extra = {
            "method": "get_device_readings",
            "service": "reading_repository",
            "device_id": device_id,
        }

        query = select(Reading).where(Reading.device_id == device_id)

        logger.debug(f"(repository) Getting readings with device_id = {device_id}", extra=logs_extra)

        if from_date:
            query = query.where(Reading.received_at >= from_date)
        if to_date:
            query = query.where(Reading.received_at <= to_date)

        query = query.order_by(Reading.received_at.desc()).limit(limit)

        result = await self.session.execute(query)
        readings = result.scalars().all()

        if readings:
            readings_list = []
            for reading in readings:
                readings_list.append(
                    ReadingResponse(
                        id=reading.id,
                        device_id=reading.device_id,
                        x=reading.x,
                        y=reading.y,
                        z=reading.z,
                        received_at=reading.received_at,
                    )
                )
            return ReadingResponseList(
                count=len(readings),
                readings=readings_list,
            )
        return ReadingResponseList(
            count=len(readings),
            readings=[],
        )
