import uuid

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import User
from app.logging.config import logger
from app.schemas import UserResponse


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, username: str) -> UserResponse:
        logs_extra = {
            "method": "create_user",
            "service": "user_repository",
            "user_name": username,
        }

        user = User(
            name=username,
        )

        logger.debug(f"(repository) Creating user with name: {username}", extra=logs_extra)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return UserResponse.model_validate(user)

    async def get_user(self, user_id: uuid.UUID) -> UserResponse | None:
        logs_extra = {
            "method": "get_user",
            "service": "user_repository",
            "user_id": user_id,
        }

        query = select(User).where(User.id == user_id)

        logger.debug(f"(repository) Getting user with id = {user_id}", extra=logs_extra)

        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return None

        await self.update_last_used(user_id=user_id)
        await self.session.refresh(user)

        user_data = {
            "id": user.id,
            "name": user.name,
            "created_at": user.created_at,
            "last_used": user.last_used,
        }

        return UserResponse.model_validate(user_data)

    async def update_last_used(self, user_id: uuid.UUID) -> None:
        logs_extra = {
            "method": "update_last_used",
            "service": "user_repository",
            "user_id": user_id,
        }

        user = await self.session.get(User, user_id)
        if not user:
            return None

        await self.session.execute(update(User).where(User.id == user_id).values(last_used=func.now()))
        await self.session.commit()

        logger.debug(f"(repository) Updated last_used where user_id = {user_id}", extra=logs_extra)
        return None
