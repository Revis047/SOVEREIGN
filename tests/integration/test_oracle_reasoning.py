import pytest
import asyncio
from python.agent_logic.oracle import OracleAgent

class MockSystem:
    async def get_full_state(self):
        return {
            "revenue_24h": 12000,
            "status": "OMNIPOTENT",
            "wallet": [{"symbol": "USDC", "balance": 5000}]
        }

@pytest.mark.asyncio
async def test_oracle_reasoning_loop():
    oracle = OracleAgent()
    system = MockSystem()

    # We test a single reasoning/optimization cycle instead of an infinite loop
    state = await system.get_full_state()
    reasoning = await oracle.reasoner.reason("Optimize growth", state)

    assert reasoning.confidence > 0
    assert "Neural" in reasoning.conclusion

    optimal_price = oracle.optimizer.optimize_pricing(
        price_points=[10, 20, 30],
        demand_estimates=[0.9, 0.5, 0.2],
        costs=[2, 2, 2]
    )
    assert optimal_price in [10, 20, 30]
