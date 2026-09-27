from src.services.assessment.evaluator import AssessmentEvaluator
from src.services.dag.engine import DAGEngine
from src.schemas.assessment import CriterionEvaluation, StructuredRubricParse


def test_deterministic_scoring_from_rubric():
    engine = DAGEngine(alpha=0.30, mastery_threshold=0.70)
    evaluator = AssessmentEvaluator(dag_engine=engine)

    criteria = [
        CriterionEvaluation(criterion_id="c1", criterion_title="Title 1", is_satisfied=True, weight=1.0),
        CriterionEvaluation(criterion_id="c2", criterion_title="Title 2", is_satisfied=False, weight=1.0),
    ]

    # Satisfied weight = 1.0 out of 2.0 = 0.50 ratio
    # Score = 0.50 * 0.85 + 1.0 * 0.15 = 0.425 + 0.15 = 0.575
    score = evaluator.compute_deterministic_score(criteria, architectural_soundness=1.0)
    assert score == 0.575


def test_process_evaluation_transition():
    engine = DAGEngine(alpha=0.30, mastery_threshold=0.70)
    evaluator = AssessmentEvaluator(dag_engine=engine)

    parsed = StructuredRubricParse(
        criteria_evaluations=[
            CriterionEvaluation(criterion_id="c1", criterion_title="Req 1", is_satisfied=True, weight=1.0),
            CriterionEvaluation(criterion_id="c2", criterion_title="Req 2", is_satisfied=True, weight=1.0),
        ],
        architectural_soundness_ratio=1.0,
        summary_feedback="All criteria met perfectly.",
        detected_anti_patterns=[]
    )

    result = evaluator.process_evaluation_transition(
        skill_id="rag.hybrid_fts",
        current_mastery=0.60,
        parsed_rubric=parsed,
        attempt_id="att-1"
    )

    # Raw score = 1.0
    # Updated mastery = 0.3 * 1.0 + 0.7 * 0.60 = 0.30 + 0.42 = 0.72
    assert result.raw_score == 1.0
    assert result.updated_mastery == 0.72
    # Threshold is 0.70, previous was 0.60 -> unlocked!
    assert result.mastery_unlocked is True
