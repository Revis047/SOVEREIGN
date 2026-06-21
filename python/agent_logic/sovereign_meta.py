import structlog
from typing import List, Dict, Any
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class FragilityReport(BaseModel):
    niche_concentration: float # 0-1, lower is better
    platform_dependency: Dict[str, float]
    anti_fragility_score: float

class AntiFragilityLayer:
    """
    Sub-module: Anti-Fragility.
    Ensures disruption in one stream strengthens others.
    """
    def __init__(self):
        self.streams = []

    def evaluate_risk(self, active_units: List[Dict[str, Any]]) -> FragilityReport:
        """
        Analyzes dependencies. If 80% revenue comes from TikTok, score is low.
        """
        if not active_units:
            return FragilityReport(niche_concentration=0.0, platform_dependency={}, anti_fragility_score=1.0)

        # Mock analysis
        platforms = [u.get('platform', 'unknown') for u in active_units]
        dependency = {p: platforms.count(p) / len(platforms) for p in set(platforms)}

        concentration = max(dependency.values()) if dependency else 1.0

        return FragilityReport(
            niche_concentration=concentration,
            platform_dependency=dependency,
            anti_fragility_score=1.0 - concentration
        )

    def recommend_diversification(self, report: FragilityReport) -> List[str]:
        """
        Suggests new niches/platforms to increase anti-fragility.
        """
        recommendations = []
        for platform, dep in report.platform_dependency.items():
            if dep > 0.5:
                recommendations.append(f"Diversify away from {platform} - dependency too high ({dep*100}%)")
        return recommendations

class StrategicSilence:
    """
    Sub-module: Strategic Silence Protocol.
    Manages the 'method vs output' visibility.
    """
    def __init__(self):
        self.stealth_mode = True

    def toggle_stealth(self, active: bool):
        self.stealth_mode = active
        logger.info("StrategicSilence: Stealth mode toggled", active=active)

    def filter_public_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Redacts internal methods (Pheromones, QUBO params) from public APIs/feeds.
        """
        if self.stealth_mode:
            # Remove keys that reveal strategy
            redacted = {k: v for k, v in data.items() if k not in ['strategy', 'pheromone_trail', 'qubo_energy']}
            return redacted
        return data
