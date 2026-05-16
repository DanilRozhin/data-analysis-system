import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.database.annotations import UUID_PK, CREATED_AT

if TYPE_CHECKING:
    from app.database.models.device import Device


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID_PK]
    name: Mapped[str] = mapped_column(
        nullable=False,
    )
    created_at: Mapped[CREATED_AT]
    last_used: Mapped[datetime.datetime] = mapped_column(
        nullable=True,
        server_default=func.now(),
    )

    devices: Mapped[list["Device"]] = relationship(
        back_populates="user",
    )
