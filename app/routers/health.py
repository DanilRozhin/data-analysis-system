from fastapi import APIRouter

from app.logging.config import logger

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/check", status_code=200, summary="Health check")
async def health():
    """Health check endpoint to see if app is working"""
    logger.debug("Health check called and it is healthy")
    return {
        "status": "ok",
        "message": "Service is working",
    }
