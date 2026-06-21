import structlog
from typing import List, Dict, Any, Tuple
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

logger = structlog.get_logger(__name__)

class FailureCategory(str, Enum):
    MARKET = "wrong_niche_timing"
    PRODUCT = "wrong_format_price"
    CONTENT = "wrong_platform_angle"
    OUTREACH = "wrong_score_threshold"
    EXECUTION = "infra_technical_error"

class FailureRecord(BaseModel):
    timestamp: datetime
    category: FailureCategory
    attempted_action: str
    expected_outcome: str
    actual_outcome: str
    root_cause: str
    cost_usd: float

class FailurePatternMemory:
    """
    Module 7: Failure Pattern Memory.
    """
    def __init__(self):
        self.failure_log: List[FailureRecord] = []

    def record_failure(self, record: FailureRecord):
        logger.error("FailureMemory: New failure captured", category=record.category)
        self.failure_log.append(record)

    def validate_new_idea(self, idea_meta: Dict[str, Any]) -> Tuple[bool, float]:
        matching_failures = [f for f in self.failure_log if f.root_cause in str(idea_meta)]
        if matching_failures: return False, -20.0
        return True, 10.0
