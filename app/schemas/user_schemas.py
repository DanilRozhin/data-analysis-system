import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str = Field(
        ...,
        description="User name",
    )


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: uuid.UUID = Field(
        ...,
        description="Unique User ID",
    )
    created_at: datetime.datetime = Field(
        ...,
        description="Time the User was created at",
    )
    last_used: datetime.datetime = Field(
        ...,
        description="Last User Action Time",
    )

    model_config = ConfigDict(from_attributes=True)
