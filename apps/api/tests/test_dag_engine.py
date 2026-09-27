import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.dag.engine import DAGEngine


class TestDagEngine(unittest.TestCase):

    def test_dag_engine_cycle_detection(self):
        engine = DAGEngine()
        engine.add_skill("skill_a", "Skill A", "domain_1")
        engine.add_skill("skill_b", "Skill B", "domain_1")
        engine.add_prerequisite("skill_a", "skill_b")

        # Introducing cycle must raise ValueError
        with self.assertRaises(ValueError):
            engine.add_prerequisite("skill_b", "skill_a")

    def test_ema_mastery_calculation(self):
        engine = DAGEngine(alpha=0.30)
        
        # First attempt: baseline initialization
        m1 = engine.calculate_ema_mastery(previous_mastery=0.0, raw_score=0.80)
        self.assertEqual(m1, 0.80)

        # Second attempt: 0.3 * 0.90 + 0.7 * 0.80 = 0.27 + 0.56 = 0.83
        m2 = engine.calculate_ema_mastery(previous_mastery=m1, raw_score=0.90)
        self.assertEqual(m2, 0.83)

        # Third attempt: raw score drops to 0.40 -> 0.3 * 0.40 + 0.7 * 0.83 = 0.12 + 0.581 = 0.701
        m3 = engine.calculate_ema_mastery(previous_mastery=m2, raw_score=0.40)
        self.assertEqual(m3, 0.701)

    def test_prerequisite_unlock_logic(self):
        engine = DAGEngine(mastery_threshold=0.70)
        engine.add_skill("python", "Python", "swe")
        engine.add_skill("fastapi", "FastAPI", "swe")
        engine.add_prerequisite("python", "fastapi", required_score=0.70)

        # When python is not mastered
        masteries = {"python": 0.65}
        self.assertFalse(engine.is_skill_unlocked("fastapi", masteries))

        # When python reaches threshold
        masteries["python"] = 0.75
        self.assertTrue(engine.is_skill_unlocked("fastapi", masteries))

    def test_topological_roadmap_generation(self):
        engine = DAGEngine()
        engine.add_skill("math", "Math", "ai")
        engine.add_skill("transformers", "Transformers", "ai")
        engine.add_skill("agents", "Agents", "ai")
        engine.add_prerequisite("math", "transformers")
        engine.add_prerequisite("transformers", "agents")

        roadmap = engine.generate_topological_roadmap(target_goal="agents")
        self.assertEqual(roadmap, ["math", "transformers", "agents"])


if __name__ == "__main__":
    unittest.main()
