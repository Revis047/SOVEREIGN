import asyncio
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import structlog
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http import models

logger = structlog.get_logger(__name__)

class TrailType(Enum):
    REVENUE = "revenue"
    DANGER = "danger"
    DISCOVERY = "discovery"
    EXPERTISE = "expertise"
    CUSTOMER = "customer"

class TrailSignal(BaseModel):
    trail_type: TrailType
    strength: float
    gradient_direction: List[float]
    metadata: Dict[str, Any] = {}

class PheromoneVectorEngine:
    """
    Manages stigmergic coordination trails in high-dimensional embedding space.
    Uses Qdrant as the primary vector store for pheromone persistence.
    """
    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "pheromone_trails",
        embedding_dim: int = 1536
    ):
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self._setup_collection()
        logger.info("Pheromone Engine: Initialized", qdrant=qdrant_url)

    def _setup_collection(self):
        """Ensure Qdrant collection exists with proper configuration."""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.embedding_dim,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info("Pheromone Engine: Collection Created", name=self.collection_name)
        except Exception as e:
            logger.warning("Pheromone Engine: Collection setup deferred", error=str(e))

    async def deposit_trail(
        self,
        agent_id: str,
        trail_type: TrailType,
        context_embedding: np.ndarray,
        strength: float,
        metadata: Dict[str, Any] = {}
    ):
        """Deposit a value-weighted pheromone signal."""
        # Scale strength for revenue events
        if trail_type == TrailType.REVENUE:
            strength *= 10.0

        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=context_embedding.tolist(),
                    payload={
                        "agent_id": agent_id,
                        "trail_type": trail_type.value,
                        "strength": strength,
                        "created_at": time.time(),
                        **metadata
                    }
                )
            ]
        )
        logger.debug("Pheromone: Trail Deposited", type=trail_type.value, agent=agent_id)

    async def follow_trails(
        self,
        current_embedding: np.ndarray,
        trail_preferences: List[TrailType],
        radius: float = 0.3
    ) -> List[TrailSignal]:
        """Search for high-value signal clusters in the local embedding neighborhood."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=current_embedding.tolist(),
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="trail_type",
                        match=models.MatchAny(any=[t.value for t in trail_preferences])
                    )
                ]
            ),
            limit=5,
            score_threshold=1.0 - radius,
            with_vectors=True
        )

        signals = []
        for hit in search_result:
            hit_vec = np.array(hit.vector)
            gradient = (hit_vec - current_embedding).tolist()

            signals.append(TrailSignal(
                trail_type=TrailType(hit.payload["trail_type"]),
                strength=hit.payload["strength"] * hit.score,
                gradient_direction=gradient,
                metadata=hit.payload
            ))

        return signals

    async def evaporate(self, global_decay: float = 0.05):
        """Cleanup old trails. Revenue trails have high persistence."""
        now = time.time()
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="created_at",
                        range=models.Range(lt=now - 3600)
                    ),
                    models.FieldCondition(
                        key="trail_type",
                        match=models.MatchValue(value=TrailType.DISCOVERY.value)
                    )
                ]
            )
        )
        logger.info("Pheromone: Evaporation Cycle Complete")

import uuid
