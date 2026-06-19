from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid
import numpy as np

class AgentRole(Enum):
    ANALYST    = "analyst"
    CREATOR    = "creator"
    SELLER     = "seller"
    RESEARCHER = "researcher"
    OPTIMIZER  = "optimizer"
    GUARDIAN   = "guardian"
    ORACLE     = "oracle"
    PHANTOM    = "phantom"

class AuthorityLevel(Enum):
    READ_ONLY = 0
    STANDARD = 1
    COMMERCIAL = 2
    FINANCIAL = 3
    STRUCTURAL = 4
    SOVEREIGN = 5

@dataclass
class SovereignAgent:
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: AgentRole = AgentRole.ANALYST
    working_memory_dim: int = 384
    plasma_ports: int = 3
    working_memory: np.ndarray = field(default_factory=lambda: np.zeros(384))
    pheromone_sensitivity: Dict[str, float] = field(default_factory=dict)
    trail_deposition_rate: float = 1.0
    revenue_weight: float = 1.0
    commercial_memory_access: bool = True
    authority_level: AuthorityLevel = AuthorityLevel.STANDARD
    action_budget_usd: float = 1.0
    hitl_threshold: float = 0.9
    success_rate: float = 0.0
    revenue_contribution: float = 0.0
    spawn_count: int = 0
