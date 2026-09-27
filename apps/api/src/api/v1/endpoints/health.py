from fastapi import APIRouter
from src.core.config import settings

router = APIRouter()


@router.get("/health", tags=["System"])
async def health_check():
    """System health check and runtime status."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }
