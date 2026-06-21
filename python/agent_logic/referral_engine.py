import structlog
from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class RewardType(str, Enum):
    DISCOUNT = "next_purchase_discount"
    BONUS_CONTENT = "bonus_content_unlock"
    REV_SHARE = "revenue_share_affiliate"
    STATUS_UPGRADE = "community_status"
    FREE_EXT = "free_access_extension"

class ReferralMechanic(BaseModel):
    product_id: str
    reward_type: RewardType
    reward_value: float
    referral_page_url: str
    sequences_generated: bool

class ReferralArchitectureEngine:
    """
    Module 2: Referral Architecture Engine.
    """
    def __init__(self):
        self.mechanics: Dict[str, ReferralMechanic] = {}

    def design_mechanic(self, product_id: str, category: str) -> ReferralMechanic:
        logger.info("ReferralEngine: Designing mechanic", id=product_id)
        reward_type = RewardType.REV_SHARE
        if category == "SaaS":
            reward_type = RewardType.FREE_EXT

        mechanic = ReferralMechanic(
            product_id=product_id,
            reward_type=reward_type,
            reward_value=20.0,
            referral_page_url=f"https://sov.ai/refer/{product_id}",
            sequences_generated=True
        )
        self.mechanics[product_id] = mechanic
        return mechanic
