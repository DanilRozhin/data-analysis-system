import uuid

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Device
from app.logging.config import logger
from app.schemas import DeviceResponse


class DeviceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_device(
        self, device_name: str, user_id: uuid.UUID, device_description: str | None = None
    ) -> DeviceResponse:
        logs_extra = {
            "method": "create_device",
            "service": "device_repository",
            "device_name": device_name,
            "user_id": user_id,
        }

        device = Device(
            name=device_name,
            user_id=user_id,
            description=device_description,
        )

        logger.debug(f"(repository) Creating device with name: {device_name} and user_id = {user_id}", extra=logs_extra)

        self.session.add(device)
        await self.session.commit()
        await self.session.refresh(device)

        return DeviceResponse.model_validate(device)

    async def get_device(self, device_id: uuid.UUID) -> DeviceResponse | None:
        logs_extra = {
            "method": "get_device",
            "service": "device_repository",
            "device_id": device_id,
        }

        query = select(Device).where(Device.id == device_id)

        logger.debug(f"(repository) Getting device with id = {device_id}", extra=logs_extra)

        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            return DeviceResponse.model_validate(user)
        return None

    async def get_user_devices(self, user_id: uuid.UUID) -> list[DeviceResponse] | None:
        logs_extra = {
            "method": "get_user_devices",
            "service": "device_repository",
            "user_id": user_id,
        }

        query = select(Device).where(Device.user_id == user_id)

        logger.debug(f"(repository) Getting user (id = {user_id}) devices", extra=logs_extra)

        result = await self.session.execute(query)
        devices = result.scalars().all()

        if devices:
            return [DeviceResponse.model_validate(device) for device in devices]
        return None

    async def update_last_reading_time(self, device_id: uuid.UUID) -> None:
        logs_extra = {
            "method": "update_last_reading_time",
            "service": "device_repository",
            "device_id": device_id,
        }

        query = update(Device).where(Device.id == device_id).values(last_reading_at=func.now())

        logger.debug(f"(repository) Updating last_reading_time for device with uuid: {device_id}", extra=logs_extra)

        await self.session.execute(query)
        await self.session.commit()
