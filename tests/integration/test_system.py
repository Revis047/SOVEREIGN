import pytest
from sovereign_init import SovereignOmega

@pytest.mark.asyncio
async def test_system_boot_and_state():
    system = SovereignOmega()
    await system.boot()
    state = await system.get_full_state()
    assert state["agents_active"] == 4
    assert state["oracle_status"] == "AWAKE"
    assert "revenue" in state
    assert "wallet" in state
