import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.core.health import router as health_router
from src.core.logging import configure_logging
from src.core.middleware import register_middlewares
from src.core.storage.storage_service import StorageService
from src.modules.analytics.router import router as analytics_router
from src.modules.assistant.router import router as assistant_router
from src.modules.auth.router import router as auth_router
from src.modules.conversations.router import router as conversation_router
from src.modules.data.router import router as data_router
from src.modules.forecast.router import router as forecast_router
from src.modules.knowledge.router import router as knowledge_router
from src.modules.prediction.router import router as prediction_router
from src.modules.risk.router import router as risk_router
from src.modules.tenants.router import router as tenant_router
from src.modules.users.router import router as users_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Execute application startup and shutdown tasks.
    """

    configure_logging()

    logger.info("=" * 80)
    logger.info("Starting %s", settings.app_name)
    logger.info("=" * 80)

    logger.info("Environment : %s", settings.environment)
    logger.info("Log Level   : %s", settings.log_level)

    logger.info("Initializing storage service...")

    storage = StorageService()

    try:
        storage.ensure_bucket_exists()
        logger.info("MinIO bucket verified.")
    except Exception as exc:
        logger.exception("Failed to initialize MinIO.")
        raise RuntimeError("MinIO is unavailable.") from exc

    logger.info("Application startup completed successfully.")

    yield

    logger.info("=" * 80)
    logger.info("Shutting down %s", settings.app_name)
    logger.info("Shutdown completed successfully.")
    logger.info("=" * 80)


app = FastAPI(
    title="SynapseOS API",
    version="1.0.0",
    openapi_version="3.0.3",
    lifespan=lifespan,
)

register_exception_handlers(app)
register_middlewares(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",

        # Production
        "https://synapseos.it.com",
        "https://www.synapseos.it.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "SynapseOS API Running"}


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(users_router)
app.include_router(data_router)
app.include_router(forecast_router)
app.include_router(knowledge_router)
app.include_router(assistant_router)
app.include_router(analytics_router)
app.include_router(prediction_router)
app.include_router(risk_router)
app.include_router(conversation_router)