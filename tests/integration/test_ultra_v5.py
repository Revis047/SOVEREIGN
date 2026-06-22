import pytest
from python.agent_logic.oracle import OracleAgent
from python.agent_logic.treasury_hedge import TreasuryHedge
from python.agent_logic.innovation_scanner import InnovationScanner

@pytest.mark.asyncio
async def test_metacognition_logic():
    oracle = OracleAgent()
    # Mock some reflection history
    oracle.reflection_history.append(type('obj', (object,), {'current_thought': 'Test thought'})())

    await oracle._perform_metacognition()
    assert len(oracle.reflection_history) == 2
    assert "Review of 'Test thought'" in oracle.reflection_history[-1].current_thought

def test_treasury_hedge():
    hedge = TreasuryHedge()
    orders = hedge.evaluate_risk({"volatility": "HIGH"})
    assert len(orders) == 1
    assert orders[0].asset == "ETH"

    hedge.execute_hedge(orders)
    assert hedge.portfolio["ETH"] > 0

@pytest.mark.asyncio
async def test_innovation_scanner():
    scanner = InnovationScanner()
    findings = await scanner.scan_github(["QUBO"])
    assert len(findings) > 0
    assert findings[0].tech_name == "Fast-SBM"

    absorbed = scanner.propose_absorption(findings[0])
    assert absorbed is True
    assert "Fast-SBM" in scanner.absorbed_tech
