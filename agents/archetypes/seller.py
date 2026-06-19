from agents.archetypes.base_agent import SovereignAgent, AgentRole, AuthorityLevel
import structlog

logger = structlog.get_logger(__name__)

class SellerAgent(SovereignAgent):
    def __init__(self, agent_id: str = None):
        super().__init__(
            agent_id=agent_id or "seller_1",
            role=AgentRole.SELLER,
            authority_level=AuthorityLevel.COMMERCIAL
        )
        self.pheromone_sensitivity = {"customer": 1.0, "revenue": 1.0}

    async def outreach(self, contact: str):
        logger.info("Seller: Initiating Outreach", contact=contact)
        return "Transaction Initiated"
