import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column

CREATED_AT = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
    ),
]
