import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.services.assessment.evaluator import AssessmentEvaluator
    from src.services.dag.engine import DAGEngine
    from src.schemas.assessment import CriterionEvaluation, StructuredRubricParse
except ImportError:
    AssessmentEvaluator = None


class TestAssessment(unittest.TestCase):

    def test_deterministic_scoring_from_rubric(self):
        if AssessmentEvaluator is None:
            self.skipTest("pydantic not installed in global environment")

        engine = DAGEngine(alpha=0.30, mastery_threshold=0.70)
        evaluator = AssessmentEvaluator(dag_engine=engine)

        criteria = [
            CriterionEvaluation(criterion_id="c1", criterion_title="Title 1", is_satisfied=True, weight=1.0),
            CriterionEvaluation(criterion_id="c2", criterion_title="Title 2", is_satisfied=False, weight=1.0),
        ]

        score = evaluator.compute_deterministic_score(criteria, architectural_soundness=1.0)
        self.assertEqual(score, 0.575)

    def test_process_evaluation_transition(self):
        if AssessmentEvaluator is None:
            self.skipTest("pydantic not installed in global environment")

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

        self.assertEqual(result.raw_score, 1.0)
        self.assertEqual(result.updated_mastery, 0.72)
        self.assertTrue(result.mastery_unlocked)


if __name__ == "__main__":
    unittest.main()
