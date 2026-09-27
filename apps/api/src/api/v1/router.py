from fastapi import APIRouter
from src.api.v1.endpoints import (
    health,
    dag,
    roadmap,
    retrieval,
    chat,
    assessment,
    research
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="", tags=["System"])
api_router.include_router(dag.router, prefix="/dag", tags=["Skill Graph"])
api_router.include_router(roadmap.router, prefix="/roadmap", tags=["Roadmap"])
api_router.include_router(retrieval.router, prefix="/retrieval", tags=["Retrieval"])
api_router.include_router(chat.router, prefix="/chat", tags=["Grounded Chat"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
api_router.include_router(research.router, prefix="/research", tags=["Web Research"])
