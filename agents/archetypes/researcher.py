from agents.archetypes.base_agent import SovereignAgent, AgentRole, AuthorityLevel
import structlog

logger = structlog.get_logger(__name__)

class ResearcherAgent(SovereignAgent):
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "researcher_1",
            role=AgentRole.RESEARCHER,
            authority_level=AuthorityLevel.STANDARD
        )
        self.pheromone_sensitivity = {"discovery": 1.0, "expertise": 1.0}

    async def deep_dive(self, topic: str):
        logger.info("Researcher: Deep Dive", topic=topic)
        return "Insight Extraction Complete"
