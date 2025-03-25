import uvicorn
from fastapi import FastAPI

from app.api.routers import api_router
import app.config.logger as logger
from app.config.settings import settings
from app.system.middlewares.content_type import ContentTypeMiddleware


def prepare_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP.NAME,
        openapi_prefix=settings.APP.OPENAPI_PREFIX,
        version=settings.APP.VERSION,
    )
    app.include_router(api_router)
    app.add_middleware(ContentTypeMiddleware)
    return app


def start_service() -> None:
    uvicorn.run(
        prepare_app(),
        host=settings.APP.ADDRESS,
        port=settings.APP.PORT,
        log_config=logger.get_uvicorn_log_config(
            {"formatters": {"default": {"()": settings.APP.LOG_DEFAULT_FORMATTER}}},
        ),
        access_log=False,
    )


if __name__ == "__main__":
    start_service()