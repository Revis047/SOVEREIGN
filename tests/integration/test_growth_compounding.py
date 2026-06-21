import pytest
import asyncio
from python.agent_logic.oracle import OracleAgent

@pytest.mark.asyncio
async def test_growth_modules_initialization():
    oracle = OracleAgent()

    # 1. Test Emotional Mapping
    sig = oracle.emotional_mapping.analyze_icp_language("icp_1", ["stuck", "obsolete"])
    assert sig.intensity > 0.5

    # 2. Test Referral Engine
    mech = oracle.referral_engine.design_mechanic("prod_1", "SaaS")
    assert mech.reward_type == "free_access_extension"

    # 3. Test Topical Authority
    tree = oracle.topical_authority.map_topic_tree("niche_a", "AI CFO")
    assert len(tree) >= 3

    # 4. Test LTV Maximizer
    risk = oracle.ltv_maximizer.check_churn_risk(
        oracle.ltv_maximizer.customers.get("c1",
        type('obj', (object,), {'customer_id': 'c1', 'engagement_metrics': {'login_freq': 0.1}, 'products_purchased': []}))
    )
    assert risk >= 0.5

    # 5. Test Geo Arbitrage
    regions = oracle.geo_arbitrage.rank_arbitrage_opportunities(0.1)
    assert regions[0].name in ["MENA", "LATAM", "Brazil", "East Africa"]
