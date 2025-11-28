from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.telemetry import init_tracing

settings = get_settings()
setup_logging()
init_tracing()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)

    origins = settings.backend_cors_origins if isinstance(settings.backend_cors_origins, list) else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Instrumentator().instrument(app).expose(app)
    app.include_router(api_router)

    @app.get("/", tags=["health"])  # pragma: no cover
    async def root() -> dict[str, str]:
        return {"message": "SIAD Agro API operacional"}

    return app


app = create_app()
