import uuid
from fastapi import APIRouter
from src.schemas.assessment import (
    AssessmentSubmission,
    AssessmentResult,
    StructuredRubricParse,
    CriterionEvaluation
)
from src.services.assessment.evaluator import AssessmentEvaluator
from src.services.dag.taxonomy import build_canonical_graph

router = APIRouter()
dag_engine = build_canonical_graph()
evaluator = AssessmentEvaluator(dag_engine=dag_engine)


@router.post("/submit", response_model=AssessmentResult, tags=["Assessment"])
async def submit_assessment(submission: AssessmentSubmission):
    """
    Evaluates assessment submission deterministically via Pydantic rubric parsing + EMA update.
    """
    attempt_id = str(uuid.uuid4())
    current_mastery = 0.50  # Mock current baseline

    # Simulate structured rubric parse (which is returned by LLM grammar-constrained decoding)
    parsed_rubric = StructuredRubricParse(
        criteria_evaluations=[
            CriterionEvaluation(
                criterion_id="crit_1",
                criterion_title="Implementation of k=60 RRF reciprocal ranking",
                is_satisfied=True,
                evidence_quote="scores[doc_id] += 1.0 / (60 + rank)",
                weight=1.0
            ),
            CriterionEvaluation(
                criterion_id="crit_2",
                criterion_title="Post-retrieval cross-encoder reranking pass",
                is_satisfied=True,
                evidence_quote="CrossEncoderReranker().rerank(candidates)",
                weight=1.0
            ),
            CriterionEvaluation(
                criterion_id="crit_3",
                criterion_title="Handling empty candidate lists gracefully",
                is_satisfied=True,
                evidence_quote="if not candidates: return []",
                weight=0.5
            )
        ],
        architectural_soundness_ratio=0.95,
        summary_feedback="Strong implementation! Explicitly adheres to ADR 003 specifications with proper smoothing constant and fallback bounds.",
        detected_anti_patterns=[]
    )

    result = evaluator.process_evaluation_transition(
        skill_id=submission.skill_id,
        current_mastery=current_mastery,
        parsed_rubric=parsed_rubric,
        attempt_id=attempt_id
    )

    return result
