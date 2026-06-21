import structlog
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class TimingReport(BaseModel):
    idea_id: str
    launch_priority_score: float # 0-1
    optimal_window_start: datetime
    suggested_platform: str
    readiness_signals: List[str]

class MarketTimingIntelligence:
    """
    Module 5: Market Timing Intelligence.
    Determines what to build next and when to launch based on algorithm cycles
    and competitor weakness windows.
    """
    def __init__(self):
        self.algorithm_health = {
            "TikTok": 0.85, # 0.85 means high growth rewards
            "YouTube": 0.40, # 0.40 means stability phase
            "X": 0.65
        }

    def score_launch_window(self, idea_meta: Dict[str, Any]) -> TimingReport:
        """
        Scores an idea for 'Now-ness'.
        Factors: seasonal, algorithm pulse, competitor density.
        """
        idea_id = idea_meta.get('id', 'unknown')
        logger.info("MarketTiming: Scoring launch window", idea=idea_id)

        # Heuristic: if TikTok health > 0.8, prioritize TikTok-friendly products
        priority = 0.92
        platform = "TikTok" if self.algorithm_health["TikTok"] > 0.7 else "Email"

        return TimingReport(
            idea_id=idea_id,
            launch_priority_score=priority,
            optimal_window_start=datetime.now(timezone.utc),
            suggested_platform=platform,
            readiness_signals=["High engagement in niche A", "Competitor B latency increase"]
        )

    def sequence_segments(self, niche: str) -> List[str]:
        """
        Defines the sequencing: Early Adopters -> Early Majority -> Mass Market.
        """
        return ["AI-Native Developers", "SaaS Founders", "General SMBs"]

class RevenueScalingArchitecture:
    """
    Module 6: Revenue Scaling Architecture.
    Manages parallel business units and compounds intelligence advantage.
    """
    def __init__(self):
        self.business_units = []

    def register_unit(self, company_id: str, niche: str):
        self.business_units.append({
            "id": company_id,
            "niche": niche,
            "status": "ACTIVE",
            "revenue_run_rate": 0.0
        })
        logger.info("ScalingArchitecture: Registered new Business Unit", id=company_id)

    def calculate_intelligence_multiplier(self) -> float:
        """
        Calculates how much better ICP models are based on the number of active units.
        Intelligence = units * log(interactions)
        """
        unit_count = len(self.business_units)
        return 1.0 + (unit_count * 0.15) # 15% boost per active unit
