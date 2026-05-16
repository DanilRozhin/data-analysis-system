import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository
from app.schemas import UserResponse


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session=session)

    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        try:
            user = await self.user_repo.get_user(user_id=user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {user_id} not found")
            return user

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e

    async def create_user(self, username: str) -> UserResponse:
        try:
            return await self.user_repo.create_user(username=username)

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            ) from e
