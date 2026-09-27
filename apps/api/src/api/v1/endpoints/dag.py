from fastapi import APIRouter, HTTPException
from src.services.dag.taxonomy import INITIAL_TAXONOMY, build_canonical_graph
from src.schemas.dag import SkillGraphResponse

router = APIRouter()


@router.get("/graph", response_model=SkillGraphResponse, tags=["Skill Graph"])
async def get_skill_graph():
    """Returns the complete Directed Acyclic Graph topology for Cytoscape visualization."""
    engine = build_canonical_graph()
    
    nodes = []
    edges = []
    
    for skill in INITIAL_TAXONOMY:
        nodes.append({
            "data": {
                "id": skill["id"],
                "label": skill["name"],
                "domain": skill["domain"],
                "depth": skill["depth_level"],
                "threshold": skill["mastery_threshold"],
                "description": skill["description"]
            }
        })
        for prereq in skill["prerequisites"]:
            edges.append({
                "data": {
                    "id": f"{prereq}->{skill['id']}",
                    "source": prereq,
                    "target": skill["id"],
                    "label": f"requires {prereq}"
                }
            })

    return SkillGraphResponse(
        nodes=nodes,
        edges=edges,
        total_skills=len(nodes)
    )


@router.get("/skills/{skill_id}", tags=["Skill Graph"])
async def get_skill_detail(skill_id: str):
    """Retrieve detailed metadata, prerequisites, and rubric thresholds for a single node."""
    for skill in INITIAL_TAXONOMY:
        if skill["id"] == skill_id:
            return skill
    raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found in DAG taxonomy")
