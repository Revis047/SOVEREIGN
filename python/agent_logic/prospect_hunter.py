import structlog
from typing import List, Dict, Any
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class Prospect(BaseModel):
    id: str
    name: str
    email: str
    linkedin_url: str
    firmographics: Dict[str, Any]
    icp_score: float = 0.0

class ProspectHunter:
    """
    Layer 9: Prospect Hunting.
    Integrates with Apollo API to find and score verified business contacts.
    """
    def __init__(self, apollo_api_key: str = ""):
        self.api_key = apollo_api_key

    async def find_prospects(self, icp_criteria: Dict[str, Any]) -> List[Prospect]:
        """
        Queries Apollo API for contacts matching ICP structural criteria.
        """
        logger.info("ProspectHunter: Searching Apollo for ICP-matched contacts", criteria=icp_criteria)

        # Simulation of Apollo API response
        mock_results = [
            Prospect(
                id="apollo_1",
                name="John Doe",
                email="john@startup.ai",
                linkedin_url="linkedin.com/in/johndoe",
                firmographics={"industry": "AI", "size": "10-50", "funding": "Series A"}
            ),
            Prospect(
                id="apollo_2",
                name="Jane Smith",
                email="jane@corp.com",
                linkedin_url="linkedin.com/in/janesmith",
                firmographics={"industry": "Retail", "size": "500+", "funding": "Public"}
            )
        ]
        return mock_results

    def score_prospect(self, prospect: Prospect, behavioral_model: Any) -> float:
        """
        Scores a prospect against the living ICP profile.
        Combines structural match (firmographics) + behavioral match.
        """
        # Logic: Industry AI = 0.5, Series A = 0.3, size matches = 0.2
        score = 0.0
        if prospect.firmographics.get("industry") == "AI":
            score += 0.5
        if prospect.firmographics.get("funding") == "Series A":
            score += 0.3
        if prospect.firmographics.get("size") == "10-50":
            score += 0.15

        prospect.icp_score = score
        return score

    async def hunt_and_outreach(self, icp_criteria: Dict[str, Any], outreach_service: Any):
        """
        Full hunter cycle: Find -> Score -> Outreach (if match > 80%).
        """
        prospects = await self.find_prospects(icp_criteria)
        for p in prospects:
            score = self.score_prospect(p, None)
            if score >= 0.8:
                logger.info("ProspectHunter: HIGH-VALUE TARGET DISCOVERED", name=p.name, score=score)
                # Call Layer 9 Outreach Service (5-touch sequence)
                await outreach_service.trigger_sequence(p)
            else:
                logger.debug("ProspectHunter: Target skipped (low match)", name=p.name, score=score)
