from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.core.config import settings

router = APIRouter()


class ResearchQuery(BaseModel):
    query: str
    max_results: int = 5


class ResearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    source: str


@router.post("/query", response_model=ResearchResponse, tags=["Web Research"])
async def execute_research(req: ResearchQuery):
    """
    Dispatches targeted web research when freshness or evolving framework triggers fire.
    """
    if settings.TAVILY_API_KEY:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            res = client.search(query=req.query, max_results=req.max_results)
            return ResearchResponse(
                query=req.query,
                results=res.get("results", []),
                source="tavily_live"
            )
        except Exception:
            pass

    # High-quality fallback for offline / test environments
    mock_results = [
        {
            "title": f"Recent Technical Specification: {req.query}",
            "url": "https://spec.modelcontextprotocol.io/",
            "content": "Official standard guidelines on resource templates, prompt providers, and execution loops."
        }
    ]
    return ResearchResponse(
        query=req.query,
        results=mock_results,
        source="local_simulation"
    )
