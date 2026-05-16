import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class StatsResponse(BaseModel):
    min_value: float | None = Field(
        ...,
        description="The minimum value for the statistics",
    )
    max_value: float | None = Field(
        ...,
        description="The maximum value for the statistics",
    )
    readings_amount: int = Field(
        ...,
        description="The amount of device readings",
    )
    sum_value: float | None = Field(
        ...,
        description="The sum of the values in the list",
    )
    median: float | None = Field(
        ...,
        description="The median of the values in the list",
    )
    period_from: datetime.datetime | None = Field(
        default=None,
        description="The start date for the statistics",
    )
    period_to: datetime.datetime | None = Field(
        default=None,
        description="The end date for the statistics",
    )

    model_config = ConfigDict(from_attributes=True)


class DeviceStatsResponse(BaseModel):
    device_id: uuid.UUID = Field(
        ...,
        description="The device UUID",
    )
    device_name: str = Field(
        ...,
        description="The name of the device",
    )
    statistics: StatsResponse = Field(
        ...,
        description="The statistics of the device",
    )


class UserAggregatedStatsResponse(BaseModel):
    user_id: uuid.UUID = Field(
        ...,
        description="The user UUID",
    )
    total_devices: int = Field(
        ...,
        description="The total number of devices user owns",
    )
    total_readings: int = Field(
        ...,
        description="The total number of readings user devices have",
    )
    statistics: StatsResponse | None = Field(
        ...,
        description="The statistics of the user",
    )
    devices_stats: list[DeviceStatsResponse] | None = Field(
        ...,
        description="Each device statistics",
    )
