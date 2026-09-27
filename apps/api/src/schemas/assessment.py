from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CriterionEvaluation(BaseModel):
    criterion_id: str
    criterion_title: str
    is_satisfied: bool
    evidence_quote: Optional[str] = None
    flaw_explanation: Optional[str] = None
    weight: float = 1.0


class StructuredRubricParse(BaseModel):
    """Schema enforced on the LLM evaluation pass for strict deterministic parsing."""
    criteria_evaluations: List[CriterionEvaluation]
    architectural_soundness_ratio: float = Field(ge=0.0, le=1.0)
    summary_feedback: str
    detected_anti_patterns: List[str] = Field(default_factory=list)


class AssessmentSubmission(BaseModel):
    skill_id: str
    question_prompt: str
    user_code_or_answer: str


class AssessmentResult(BaseModel):
    attempt_id: str
    skill_id: str
    raw_score: float
    previous_mastery: float
    updated_mastery: float
    mastery_unlocked: bool
    rubric_breakdown: List[CriterionEvaluation]
    feedback: str
    next_recommended_skill: Optional[str] = None
