import structlog
from typing import List, Dict, Any, Tuple
from enum import Enum
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class EmotionalCategory(str, Enum):
    FEAR_BEHIND = "fear_left_behind"
    FEAR_MISSING = "fear_missing_out"
    FEAR_FAILURE = "fear_failure"
    FEAR_IRRELEVANCE = "fear_irrelevance"
    DESIRE_STATUS = "desire_status"
    DESIRE_BELONGING = "desire_belonging"
    DESIRE_CONTROL = "desire_control"
    DESIRE_FREEDOM = "desire_freedom"
    IDENTITY_IDEAL = "identity_aspiration"
    IDENTITY_AVOID = "identity_avoidance"

class EmotionalSignature(BaseModel):
    primary: EmotionalCategory
    secondary: EmotionalCategory
    intensity: float # 0-1
    keywords: List[str]

class EmotionalTriggerDetector:
    """
    Module 1: Emotional Trigger Mapping.
    """
    def __init__(self):
        self.emotional_map: Dict[str, EmotionalSignature] = {}

    def analyze_icp_language(self, icp_id: str, language_patterns: List[str]) -> EmotionalSignature:
        logger.info("EmotionalTrigger: Analyzing ICP language patterns", icp=icp_id)
        text = " ".join(language_patterns).lower()
        if "stuck" in text or "control" in text:
            primary = EmotionalCategory.DESIRE_CONTROL
        elif "future" in text or "obsolete" in text:
            primary = EmotionalCategory.FEAR_IRRELEVANCE
        else:
            primary = EmotionalCategory.DESIRE_FREEDOM

        sig = EmotionalSignature(
            primary=primary,
            secondary=EmotionalCategory.DESIRE_STATUS,
            intensity=0.85,
            keywords=["freedom", "winning"]
        )
        self.emotional_map[icp_id] = sig
        return sig

    def tag_content(self, content_id: str, icp_id: str, raw_content: str) -> str:
        sig = self.emotional_map.get(icp_id)
        if not sig: return raw_content
        return f"[EMOTIONAL_TRIGGER: {sig.primary}] {raw_content}"

    def update_map_from_conversions(self, conversion_data: List[Dict[str, Any]]):
        """
        Refines the emotional map every 30 days based on real conversion performance.
        """
        logger.info("EmotionalTrigger: Updating map from latest conversion data", samples=len(conversion_data))

        # Aggregate CVR per emotional trigger
        stats = {}
        for conv in conversion_data:
            trigger = conv.get('trigger')
            if not trigger: continue
            if trigger not in stats: stats[trigger] = {'wins': 0, 'total': 0}
            stats[trigger]['total'] += 1
            if conv.get('converted'): stats[trigger]['wins'] += 1

        # Update map with best performing triggers
        for icp_id, sig in self.emotional_map.items():
            if stats:
                best_trigger = max(stats.keys(), key=lambda t: stats[t]['wins']/stats[t]['total'])
                if best_trigger != sig.primary:
                    logger.info("EmotionalTrigger: Pivot detected", icp=icp_id, new_best=best_trigger)
                    sig.primary = best_trigger
