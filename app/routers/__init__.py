from .device import device_router
from .health import health_router
from .reading import reading_router
from .stats import stats_router
from .user import user_router

__all__ = [
    "device_router",
    "health_router",
    "reading_router",
    "stats_router",
    "user_router",
]
