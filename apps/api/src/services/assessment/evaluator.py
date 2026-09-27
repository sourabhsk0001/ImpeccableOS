from typing import List, Dict, Any, Tuple
from src.schemas.assessment import CriterionEvaluation, StructuredRubricParse, AssessmentResult
from src.services.dag.engine import DAGEngine


class AssessmentEvaluator:
    """
    Deterministic evaluation engine:
    Computes objective scores from rubric boolean criteria and updates skill mastery via EMA.
    Prevents prompt injection manipulation of mastery values.
    """

    def __init__(self, dag_engine: DAGEngine):
        self.dag_engine = dag_engine

    def compute_deterministic_score(
        self, criteria: List[CriterionEvaluation], architectural_soundness: float = 1.0
    ) -> float:
        """
        Computes weighted raw score strictly from parsed boolean criteria.
        Formula:
        Raw_Score = (sum(weight_i * is_satisfied_i) / sum(weight_i)) * 0.85 + (soundness * 0.15)
        """
        if not criteria:
            return round(architectural_soundness, 4)

        total_weight = sum(c.weight for c in criteria)
        satisfied_weight = sum(c.weight for c in criteria if c.is_satisfied)
        
        criteria_ratio = (satisfied_weight / total_weight) if total_weight > 0 else 0.0
        final_score = (criteria_ratio * 0.85) + (architectural_soundness * 0.15)
        return round(float(final_score), 4)

    def process_evaluation_transition(
        self,
        skill_id: str,
        current_mastery: float,
        parsed_rubric: StructuredRubricParse,
        attempt_id: str
    ) -> AssessmentResult:
        """
        Executes deterministic state transition and checks mastery threshold.
        """
        raw_score = self.compute_deterministic_score(
            criteria=parsed_rubric.criteria_evaluations,
            architectural_soundness=parsed_rubric.architectural_soundness_ratio
        )

        updated_mastery = self.dag_engine.calculate_ema_mastery(
            previous_mastery=current_mastery,
            raw_score=raw_score
        )

        threshold = self.dag_engine.mastery_threshold
        unlocked = (updated_mastery >= threshold) and (current_mastery < threshold)

        return AssessmentResult(
            attempt_id=attempt_id,
            skill_id=skill_id,
            raw_score=raw_score,
            previous_mastery=current_mastery,
            updated_mastery=updated_mastery,
            mastery_unlocked=unlocked,
            rubric_breakdown=parsed_rubric.criteria_evaluations,
            feedback=parsed_rubric.summary_feedback,
            next_recommended_skill=None
        )
