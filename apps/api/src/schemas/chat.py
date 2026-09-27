from typing import List, Optional
from pydantic import BaseModel, Field
from src.schemas.retrieval import ConfidenceBreakdown, RetrievedChunk


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class GroundedChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    skill_context_id: Optional[str] = None
    force_web_search: bool = False


class InlineCitation(BaseModel):
    citation_id: int
    source_title: str
    section_title: Optional[str] = None
    authority_level: int
    url: Optional[str] = None
    exact_quote: str


class GroundedChatResponse(BaseModel):
    reply: str
    citations: List[InlineCitation]
    confidence_breakdown: ConfidenceBreakdown
    retrieved_sources: List[RetrievedChunk]
    used_web_search: bool
    trace_id: str
