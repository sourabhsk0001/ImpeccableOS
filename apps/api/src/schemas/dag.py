from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SkillNodeSchema(BaseModel):
    id: str
    domain: str
    name: str
    description: str
    depth_level: int
    mastery_threshold: float = 0.70
    prerequisites: List[str] = Field(default_factory=list)


class SkillGraphResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    total_skills: int


class UserMasteryState(BaseModel):
    skill_id: str
    skill_name: str
    domain: str
    mastery_score: float
    is_unlocked: bool
    is_mastered: bool
    attempts_count: int


class RoadmapResponse(BaseModel):
    target_career_path: str
    topological_sequence: List[str]
    active_skills: List[UserMasteryState]
    mastered_skills: List[UserMasteryState]
    locked_skills: List[UserMasteryState]
    overall_completion_rate: float
