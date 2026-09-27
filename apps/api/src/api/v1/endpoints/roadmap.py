from fastapi import APIRouter
from src.services.dag.taxonomy import INITIAL_TAXONOMY, build_canonical_graph
from src.schemas.dag import RoadmapResponse, UserMasteryState

router = APIRouter()


@router.get("/user-roadmap", response_model=RoadmapResponse, tags=["Roadmap"])
async def get_user_roadmap(target_career_path: str = "Agentic AI Systems Engineer"):
    """
    Computes deterministic topological roadmap based on the learner's goal and current mastery state.
    """
    engine = build_canonical_graph()
    
    # In production, query user_skill_mastery from database
    # Here we mock default initial learner state:
    mock_masteries = {
        "swe.python_async": 0.85,
        "swe.databases": 0.72,
        "ai.vector_math": 0.78,
    }

    topo_order = engine.generate_topological_roadmap()
    mastered_ids, active_ids, locked_ids = engine.evaluate_unlocked_and_active_skills(mock_masteries)

    skill_lookup = {s["id"]: s for s in INITIAL_TAXONOMY}

    def to_state(sid: str, is_unlocked: bool, is_mastered: bool) -> UserMasteryState:
        info = skill_lookup[sid]
        return UserMasteryState(
            skill_id=sid,
            skill_name=info["name"],
            domain=info["domain"],
            mastery_score=mock_masteries.get(sid, 0.0),
            is_unlocked=is_unlocked,
            is_mastered=is_mastered,
            attempts_count=1 if sid in mock_masteries else 0
        )

    mastered_states = [to_state(sid, True, True) for sid in mastered_ids]
    active_states = [to_state(sid, True, False) for sid in active_ids]
    locked_states = [to_state(sid, False, False) for sid in locked_ids]

    total_count = len(INITIAL_TAXONOMY)
    completion = round(len(mastered_states) / max(1, total_count), 4)

    return RoadmapResponse(
        target_career_path=target_career_path,
        topological_sequence=topo_order,
        active_skills=active_states,
        mastered_skills=mastered_states,
        locked_skills=locked_states,
        overall_completion_rate=completion
    )
