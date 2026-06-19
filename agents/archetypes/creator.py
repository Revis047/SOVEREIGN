from agents.archetypes.base_agent import SovereignAgent, AgentRole, AuthorityLevel
import structlog

logger = structlog.get_logger(__name__)

class CreatorAgent(SovereignAgent):
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "creator_1",
            role=AgentRole.CREATOR,
            authority_level=AuthorityLevel.COMMERCIAL
        )
        self.pheromone_sensitivity = {"revenue": 1.0, "customer": 0.5}

    async def generate_asset(self, spec: str):
        logger.info("Creator: Generating Asset", spec=spec)
        return "Digital Product Template v1"
