import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ReadingBase(BaseModel):
    x: float = Field(..., description="The X parameter")
    y: float = Field(..., description="The Y parameter")
    z: float = Field(..., description="The Z parameter")


class ReadingCreate(ReadingBase):
    pass


class ReadingResponse(ReadingBase):
    id: uuid.UUID = Field(..., description="The UUID of the Reading")
    received_at: datetime.datetime | None = Field(..., description="The datetime when the Reading was received")
    device_id: uuid.UUID = Field(
        ...,
        description="The UUID of the device",
    )

    model_config = ConfigDict(from_attributes=True)


class ReadingResponseList(BaseModel):
    count: int = Field(
        ...,
        description="The count of Readings in the list",
    )
    readings: list[ReadingResponse] | None = Field(
        ...,
        description="The list of Readings",
    )

    model_config = ConfigDict(from_attributes=True)
