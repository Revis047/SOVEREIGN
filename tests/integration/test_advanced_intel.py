import pytest
import asyncio
from python.agent_logic.oracle import OracleAgent
from python.agent_logic.blindspot_engine import BlindspotEngine
from python.agent_logic.superposition_intelligence import SuperpositionIntelligence

class MockSystem:
    async def get_full_state(self):
        return {
            "revenue": {"daily_revenue": 5000},
            "status": "OPERATIONAL",
            "wallet": []
        }

@pytest.mark.asyncio
async def test_advanced_intel_components():
    oracle = OracleAgent()
    system = MockSystem()

    # 1. Test Blindspot
    consensus = oracle.blindspot.construct_consensus_map([])
    deviation = oracle.blindspot.compute_deviation_vector(consensus)
    gap = oracle.blindspot.score_gap(deviation, [])
    assert gap.gap_score > 0
    assert len(gap.deviation_vector) == 1536

    # 2. Test Superposition
    oracle.superposition.initialize_superposition([
        {"id": "profitable", "description": "Market is growing"},
        {"id": "saturated", "description": "Too many competitors"}
    ])
    await oracle.superposition.process_evidence({"content": "highly profitable"})
    weights = oracle.superposition.get_resource_allocation()
    assert weights["profitable"] > weights["saturated"]

    # 3. Test Sensory Cortex
    oracle.sensory_cortex.process_sensory_input({0: 0.9, 12: 0.8})
    view = oracle.sensory_cortex.get_unified_perception()
    assert view["average_consciousness_intensity"] > 0

    # 4. Test Temporal
    oracle.temporal_consciousness.integrate_past([{"signature": "growth_pattern"}])
    oracle.temporal_consciousness.update_present({"signature": "growth_pattern"})
    oracle.temporal_consciousness.project_futures({"WIN": 0.9, "LOSE": 0.1})
    context = oracle.temporal_consciousness.resolve_decision_context()
    assert context["integrated_confidence"] > 0.5
