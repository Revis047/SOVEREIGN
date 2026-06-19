import asyncio
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import structlog
from pydantic import BaseModel
from core.pheromone_economy.pheromone_engine import PheromoneVectorEngine, TrailType, TrailSignal
from agents.archetypes.base_agent import SovereignAgent

logger = structlog.get_logger(__name__)

class CoordinationPlan(BaseModel):
    assignments: Dict[str, str] # agent_id -> strategy
    landscape_summary: Dict[str, Any]

class StigmergicCoordinator:
    """
    High-level coordinator that uses pheromone signals to orchestrate
    agent behavior without explicit instruction.
    """
    def __init__(self, pheromone_engine: PheromoneVectorEngine):
        self.pheromone_engine = pheromone_engine
        logger.info("StigmergicCoordinator: Initialized")

    async def coordinate(self, agent_pool: List[SovereignAgent]) -> CoordinationPlan:
        """
        Reads the pheromone landscape and assigns agents to emergent strategies.
        """
        landscape = self.pheromone_engine.get_landscape_summary()
        logger.info("StigmergicCoordinator: Orchestrating Swarm", pool_size=len(agent_pool))

        assignments = {}
        for agent in agent_pool:
            # Query trails near the agent's current mental state
            trails = await self.pheromone_engine.follow_trails(
                agent.working_memory,
                trail_preferences=[TrailType.REVENUE, TrailType.CUSTOMER]
            )

            # Emergent Decision Logic
            revenue_signals = [t for t in trails if t.trail_type == TrailType.REVENUE]

            if revenue_signals:
                assignments[agent.agent_id] = "exploit_revenue_cluster"
            elif any(t.trail_type == TrailType.CUSTOMER for t in trails):
                assignments[agent.agent_id] = "engage_customer_gradient"
            else:
                assignments[agent.agent_id] = "stochastic_exploration"

        return CoordinationPlan(
            assignments=assignments,
            landscape_summary=landscape
        )
