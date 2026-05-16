import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import DeviceRepository, UserRepository
from app.schemas import DeviceResponse, DeviceResponseList


class DeviceService:
    def __init__(self, session: AsyncSession):
        self.device_repo = DeviceRepository(session=session)
        self.user_repo = UserRepository(session=session)

    async def get_device(self, device_id: uuid.UUID) -> DeviceResponse:
        try:
            device = await self.device_repo.get_device(device_id=device_id)
            if not device:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id = {device_id} not found"
                )
            return device

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e

    async def create_device(
        self, user_id: uuid.UUID, device_name: str, device_description: str | None = None
    ) -> DeviceResponse:
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {user_id} not found")
            return await self.device_repo.create_device(
                user_id=user_id, device_name=device_name, device_description=device_description
            )

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e

    async def get_user_devices(self, user_id: uuid.UUID) -> DeviceResponseList:
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {user_id} not found")
            return await self.device_repo.get_user_devices(user_id=user_id)

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e
