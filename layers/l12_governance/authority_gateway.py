import asyncio
from typing import List, Dict, Any, Optional
import structlog
from pydantic import BaseModel
from agents.archetypes.base_agent import SovereignAgent, AuthorityLevel

logger = structlog.get_logger(__name__)

class AgentAction(BaseModel):
    id: str
    type: str
    required_level: AuthorityLevel
    cost: float = 0.0

class AuthorityGateway:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        logger.info("AuthorityGateway: Immune System Initialized")

    async def authorize(self, agent: SovereignAgent, action: AgentAction) -> bool:
        logger.info("Governance: Authorizing Action", agent=agent.agent_id, action=action.type)
        if action.required_level.value > agent.authority_level.value:
            logger.warning("Governance: DENIED (Level)", id=agent.agent_id)
            return False
        if action.cost > agent.action_budget_usd:
            logger.warning("Governance: DENIED (Budget)", id=agent.agent_id)
            return False
        self.logs.append({"agent": agent.agent_id, "action": action.type, "status": "APPROVED"})
        return True
