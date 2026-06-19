import pytest
import asyncio
from python.omega_genesis import SovereignOmega

@pytest.mark.asyncio
async def test_omega_boot_and_revenue():
    system = SovereignOmega()
    await system.boot()

    # Wait for one generator cycle
    await asyncio.sleep(0.1)

    state = await system.get_full_state()
    assert state["agents_active"] == 12
    assert state["system_health"] == "OPTIMAL"
    assert state["revenue"]["daily_revenue"] >= 0
