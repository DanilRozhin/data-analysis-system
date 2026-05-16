import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.database import Base
from app.database.annotations import UUID_PK, CREATED_AT

if TYPE_CHECKING:
    from app.database.models.device import Device


class Reading(Base):
    __tablename__ = "reading"

    id: Mapped[UUID_PK]
    device_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "device.id",
            name="reading_device_id_fk",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    x: Mapped[float] = mapped_column(
        nullable=False,
    )
    y: Mapped[float] = mapped_column(
        nullable=False,
    )
    z: Mapped[float] = mapped_column(
        nullable=False,
    )
    received_at: Mapped[CREATED_AT]

    device: Mapped["Device"] = relationship(
        back_populates="readings",
    )
