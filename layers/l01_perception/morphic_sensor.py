import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional, Any
import uuid
import structlog
from pydantic import BaseModel, Field
from core.sovereign_bus.sovereign_bus import SovereignBus, SovereignMessage
import httpx
from bs4 import BeautifulSoup

logger = structlog.get_logger(__name__)

class PerceptionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_url: str
    source_type: str
    raw_content: str
    perception_score: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sensor_id: str

class MorphicSensor:
    def __init__(self, sensor_id: str, bus: SovereignBus):
        self.sensor_id = sensor_id
        self.bus = bus
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def sense_url(self, url: str, source_type: str = "web") -> Optional[PerceptionEvent]:
        try:
            logger.info("Perception: Ingesting", url=url)
            resp = await self.client.get(url)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, 'html.parser')
            for s in soup(["script", "style"]): s.decompose()
            text = soup.get_text(separator=' ', strip=True)

            event = PerceptionEvent(
                source_url=url,
                source_type=source_type,
                raw_content=text[:10000],
                perception_score=0.8,
                sensor_id=self.sensor_id
            )

            await self.bus.publish_fast("sovereign.perception.raw", SovereignMessage(
                sender=self.sensor_id, topic="sovereign.perception.raw", payload=event.model_dump()
            ))
            return event
        except Exception as e:
            logger.error("Perception: Failed", url=url, error=str(e))
            return None

    async def close(self):
        await self.client.aclose()
