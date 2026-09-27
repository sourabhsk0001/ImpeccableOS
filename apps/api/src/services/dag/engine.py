from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque


class DAGEngine:
    """
    Deterministic Directed Acyclic Graph engine for AI Engineering skill roadmaps.
    Features native pure-Python graph traversal with optional networkx interoperability.
    """

    def __init__(self, alpha: float = 0.30, mastery_threshold: float = 0.70):
        self.alpha = alpha
        self.mastery_threshold = mastery_threshold
        # Adjacency: source -> {target: required_score}
        self.adj: Dict[str, Dict[str, float]] = defaultdict(dict)
        # Predecessors: target -> {source: required_score}
        self.predecessors: Dict[str, Dict[str, float]] = defaultdict(dict)
        # Node metadata
        self.nodes: Dict[str, Dict[str, Any]] = {}

    def add_skill(self, skill_id: str, name: str, domain: str, threshold: Optional[float] = None):
        """Register a skill vertex in the DAG."""
        self.nodes[skill_id] = {
            "name": name,
            "domain": domain,
            "threshold": threshold or self.mastery_threshold
        }
        if skill_id not in self.adj:
            self.adj[skill_id] = {}
        if skill_id not in self.predecessors:
            self.predecessors[skill_id] = {}

    def has_path(self, start: str, end: str) -> bool:
        """Checks if a directed path exists between start and end (cycle check)."""
        visited = set()
        queue = deque([start])
        while queue:
            curr = queue.popleft()
            if curr == end:
                return True
            if curr not in visited:
                visited.add(curr)
                for neighbor in self.adj.get(curr, {}):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return False

    def add_prerequisite(self, source_skill: str, target_skill: str, required_score: Optional[float] = None):
        """
        Add directed dependency edge: target_skill requires source_skill.
        Strict cycle validation prevents cyclic state deadlocks.
        """
        if source_skill not in self.nodes:
            self.add_skill(source_skill, source_skill, "general")
        if target_skill not in self.nodes:
            self.add_skill(target_skill, target_skill, "general")

        # If adding source -> target creates cycle (i.e. path already exists target -> source)
        if self.has_path(target_skill, source_skill):
            raise ValueError(f"Adding prerequisite {source_skill} -> {target_skill} introduces a cyclic dependency!")

        score = required_score or self.mastery_threshold
        self.adj[source_skill][target_skill] = score
        self.predecessors[target_skill][source_skill] = score

    def calculate_ema_mastery(self, previous_mastery: float, raw_score: float) -> float:
        """
        Deterministic Exponential Moving Average (EMA) update:
        M_t = alpha * Score_t + (1 - alpha) * M_{t-1}
        """
        raw_score = max(0.0, min(1.0, raw_score))
        previous_mastery = max(0.0, min(1.0, previous_mastery))
        
        # If this is the initial assessment, the raw score sets baseline
        if previous_mastery == 0.0:
            updated = raw_score
        else:
            updated = (self.alpha * raw_score) + ((1.0 - self.alpha) * previous_mastery)
        
        return round(float(updated), 4)

    def is_skill_unlocked(self, skill_id: str, user_masteries: Dict[str, float]) -> bool:
        """Determines if all prerequisites for a skill are satisfied."""
        if skill_id not in self.nodes:
            return False
        
        prereqs = self.predecessors.get(skill_id, {})
        if not prereqs:
            return True  # Root vertex
        
        for prereq_id, required_score in prereqs.items():
            user_score = user_masteries.get(prereq_id, 0.0)
            if user_score < required_score:
                return False
        return True

    def get_ancestors(self, target_goal: str) -> Set[str]:
        """Returns all ancestral prerequisites required for target_goal."""
        ancestors = set()
        queue = deque([target_goal])
        while queue:
            curr = queue.popleft()
            for prereq in self.predecessors.get(curr, {}):
                if prereq not in ancestors:
                    ancestors.add(prereq)
                    queue.append(prereq)
        return ancestors

    def generate_topological_roadmap(self, target_goal: Optional[str] = None) -> List[str]:
        """
        Computes deterministic Kahn's topological sorting algorithm on the DAG.
        If target_goal is given, filters to the ancestral sub-DAG.
        """
        if target_goal and target_goal in self.nodes:
            allowed = self.get_ancestors(target_goal)
            allowed.add(target_goal)
        else:
            allowed = set(self.nodes.keys())

        # In-degree computation restricted to allowed set
        in_degree = {n: 0 for n in allowed}
        for u in allowed:
            for v in self.adj.get(u, {}):
                if v in allowed:
                    in_degree[v] += 1

        queue = deque([n for n in allowed if in_degree[n] == 0])
        ordered = []

        while queue:
            node = queue.popleft()
            ordered.append(node)
            for neighbor in self.adj.get(node, {}):
                if neighbor in allowed:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

        if len(ordered) != len(allowed):
            raise ValueError("Graph contains a cycle or invalid dependencies!")

        return ordered

    def evaluate_unlocked_and_active_skills(
        self, user_masteries: Dict[str, float]
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Returns (mastered, active_available, locked) skills according to user mastery state.
        """
        mastered: List[str] = []
        active: List[str] = []
        locked: List[str] = []

        topo_order = self.generate_topological_roadmap()
        for node in topo_order:
            score = user_masteries.get(node, 0.0)
            node_threshold = self.nodes[node].get("threshold", self.mastery_threshold)
            
            if score >= node_threshold:
                mastered.append(node)
            elif self.is_skill_unlocked(node, user_masteries):
                active.append(node)
            else:
                locked.append(node)

        return mastered, active, locked
