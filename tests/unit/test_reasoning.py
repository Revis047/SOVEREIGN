import pytest
from layers.l06_reasoning.triple_track_reasoner import TripleTrackReasoner

@pytest.mark.asyncio
async def test_triple_track_reasoning():
    reasoner = TripleTrackReasoner()
    result = await reasoner.reason("How to dominate the AI market?", {"niche": "AI"})
    assert "strategic_directive" in result
    assert "objective" in result["strategic_directive"]
    assert "conclusion" in result
