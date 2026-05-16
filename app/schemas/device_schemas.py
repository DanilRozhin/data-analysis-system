import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class DeviceBase(BaseModel):
    name: str = Field(
        ...,
        description="User name",
    )
    user_id: uuid.UUID = Field(..., description="User (Device owner) ID")
    description: str | None = Field(
        default=None,
        description="Device description",
    )


class DeviceCreate(DeviceBase):
    pass


class DeviceResponse(DeviceBase):
    id: uuid.UUID = Field(
        ...,
        description="Unique Device ID",
    )
    created_at: datetime.datetime = Field(
        ...,
        description="Time the Device was created at",
    )
    last_reading_at: datetime.datetime | None = Field(
        ...,
        description="Last Time when the Device got reading",
    )

    model_config = ConfigDict(from_attributes=True)
