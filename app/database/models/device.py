import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.database import Base
from app.database.annotations import UUID_PK, CREATED_AT

if TYPE_CHECKING:
    from app.database.models.user import User
    from app.database.models.reading import Reading


class Device(Base):
    __tablename__ = "device"

    id: Mapped[UUID_PK]
    name: Mapped[str] = mapped_column(
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "user.id",
            name="device_user_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    created_at: Mapped[CREATED_AT]
    last_reading_at: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="devices",
    )
    readings: Mapped[list["Reading"]] = relationship(
        back_populates="device",
    )
