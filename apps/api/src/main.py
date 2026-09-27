import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import engine, Base
from src.api.v1.router import api_router

logger = logging.getLogger("impeccable.startup")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown procedures."""
    # Startup: Automatically provision database schemas if connected
    try:
        # Import models so Base registers all tables
        import src.models  # noqa: F401
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schemas provisioned successfully.")
    except Exception as exc:
        logger.warning(f"Database connection deferred: {exc}. Running with in-memory state engine.")

    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=f"{settings.APP_NAME} - Intelligence Layer",
    description="Adaptive AI Engineering Trainer & Execution Engine Backend API",
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Cross-Origin Resource Sharing (CORS) Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
