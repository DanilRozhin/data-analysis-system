from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.logging.config import logger, setup_logging
from app.routers import device_router, health_router, reading_router, user_router

setup_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):  # noqa: RUF029
    logger.info("Starting the FastAPI application")
    try:
        yield
    finally:
        logger.info("Finishing the FastAPI application")


def create_app():
    app_ = FastAPI(
        title="Data Analysis System",
        version="1.0.0",
        lifespan=lifespan,
    )

    app_.include_router(health_router)
    app_.include_router(user_router)
    app_.include_router(device_router)
    app_.include_router(reading_router)

    return app_


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
