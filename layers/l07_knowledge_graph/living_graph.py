import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
import structlog
from pydantic import BaseModel, Field
from layers.l01_perception.morphic_sensor import PerceptionEvent
import spacy

logger = structlog.get_logger(__name__)

class GraphNode(BaseModel):
    id: str
    label: str
    type: str # Market, Product, Competitor, ICP, PainPoint
    properties: Dict[str, Any] = {}
    confidence: float = 1.0
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str # IS_A, BUYS, COMPETES_WITH, SOLVES
    weight: float = 1.0

class LivingKnowledgeGraph:
    """
    World model that evolves and forgets.
    Maintains relationships between entities discovered in perception events.
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            logger.warning("LivingGraph: spaCy model not found, using basic extraction")
            self.nlp = None
        logger.info("LivingKnowledgeGraph: Initialized")

    async def ingest_perception_event(self, event: PerceptionEvent):
        """Extract entities and update graph structure."""
        logger.info("LivingGraph: Ingesting Event", source=event.source_url)

        # Simple Entity Extraction (NER)
        entities = []
        if self.nlp:
            doc = self.nlp(event.raw_content[:2000])
            entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Create or update nodes
        for text, label in entities:
            node_id = text.lower().replace(" ", "_")
            if node_id not in self.nodes:
                self.nodes[node_id] = GraphNode(
                    id=node_id,
                    label=text,
                    type=label
                )
            else:
                self.nodes[node_id].confidence = min(1.0, self.nodes[node_id].confidence + 0.1)
                self.nodes[node_id].last_updated = datetime.now(timezone.utc)

    async def evolve(self):
        """Global graph evolution: decay confidence and prune orphans."""
        logger.info("LivingGraph: Evolution Cycle")
        to_delete = []
        for node_id, node in self.nodes.items():
            # Decay confidence by 1% per cycle
            node.confidence *= 0.99
            if node.confidence < 0.2:
                to_delete.append(node_id)

        for node_id in to_delete:
            del self.nodes[node_id]
            logger.info("LivingGraph: Node Forgotten", id=node_id)

    def find_commercial_paths(self, start_id: str, depth: int = 3) -> List[Dict[str, Any]]:
        """Find meaningful causal chains for the reasoning layer."""
        # Implementation would involve graph traversal (NetworkX or Nebula)
        return []
