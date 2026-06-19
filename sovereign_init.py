import asyncio
import structlog
from typing import List, Dict, Any

from core.sovereign_bus.sovereign_bus import SovereignBus, SovereignMessage
from core.cognitive_plasma.cognitive_plasma import CognitivePlasma
from core.pheromone_economy.pheromone_engine import PheromoneVectorEngine

from layers.l01_perception.morphic_sensor import MorphicSensor
from layers.l01_perception.stealth_browser import StealthBrowser
from layers.l01_perception.verification import VerificationManager
from layers.l02_memory.quantum_retriever import QuantumAssociativeRetriever
from layers.l03_swarm_cognition.pheromone_engine import StigmergicCoordinator
from layers.l04_agent_mesh.morphic_topology import MorphicTopologyManager
from layers.l05_quantum_optimizer.qubo_decision import QUBODecisionEngine
from layers.l06_reasoning.triple_track_reasoner import TripleTrackReasoner
from layers.l07_knowledge_graph.living_graph import LivingKnowledgeGraph
from layers.l09_commercial_intel.icp_engine import LivingICPEngine
from layers.l10_revenue_engine.autonomous_revenue import AutonomousRevenueEngine
from layers.l10_revenue_engine.wallet import WalletEngine
from layers.l10_revenue_engine.investment_oracle import InvestmentOracle
from layers.l10_revenue_engine.currency_factory import CurrencyFactory
from layers.l10_revenue_engine.hiring import HiringEngine
from layers.l11_brand_intelligence.content_engine import BrandIntelligenceEngine
from layers.l12_governance.authority_gateway import AuthorityGateway
from layers.l12_governance.vault import AccountVault, AccountCredentials
from layers.l13_meta_consciousness.oracle_agent import OracleAgent
from layers.l13_meta_consciousness.recursive_scout import RecursiveScout

from agents.archetypes.analyst import AnalystAgent
from agents.archetypes.creator import CreatorAgent
from agents.archetypes.seller import SellerAgent

logger = structlog.get_logger(__name__)

class SovereignOmega:
    """
    The complete, unified SOVEREIGN-Ω organism.
    Integrates all 13 layers, recursive evolution, and global investment engines.
    """
    def __init__(self):
        # Core
        self.bus = SovereignBus()
        self.plasma = CognitivePlasma()
        self.pheromone = PheromoneVectorEngine()

        # Intelligence & Reasoning
        self.reasoner = TripleTrackReasoner()
        self.optimizer = QUBODecisionEngine()
        self.graph = LivingKnowledgeGraph()

        # Perception & Verification
        self.stealth = StealthBrowser()
        self.verification = VerificationManager()
        self.perception = MorphicSensor("s1", self.bus)
        self.memory = QuantumAssociativeRetriever(plasma=self.plasma)

        # Commercial & Revenue
        self.icp = LivingICPEngine()
        self.revenue = AutonomousRevenueEngine()
        self.wallet = WalletEngine()
        self.investment = InvestmentOracle()
        self.mint = CurrencyFactory()
        self.hiring = HiringEngine()

        # Brand & Distribution
        self.brand = BrandIntelligenceEngine()

        # Governance & Security
        self.governance = AuthorityGateway()
        self.governance_vault = AccountVault()

        # Meta-Consciousness & Evolution
        self.scout = RecursiveScout()
        self.oracle = OracleAgent()

        # Orchestration
        self.coordinator = StigmergicCoordinator(pheromone_engine=self.pheromone)
        self.topology = MorphicTopologyManager(self.bus, self.plasma)

        # Agent Pool
        self.agents = [
            AnalystAgent(),
            CreatorAgent(),
            SellerAgent(),
            self.oracle
        ]

    async def boot(self):
        logger.info("SOVEREIGN-Ω: EXECUTING GENESIS SEQUENCE")

        # 1. Initialize Credentials (Mock)
        await self.governance_vault.store_credentials(AccountCredentials(
            platform="TikTok", username="sovereign_prime", password="REDACTED", email="shadow@sovereign.io"
        ))

        # 2. Start Oracle Consciousness
        asyncio.create_task(self.oracle.consciousness_loop(self, self.revenue))

        logger.info("SOVEREIGN-Ω: GENESIS BOOT COMPLETE")

        msg = SovereignMessage(
            sender="SYSTEM_BOOT",
            topic="system.boot",
            payload={"status": "ONLINE", "timestamp": str(asyncio.get_event_loop().time())}
        )
        try:
            await self.bus.publish_fast("system.boot", msg)
        except Exception:
            logger.warning("Bus: Fast publish failed during boot (likely disconnected)")

    async def get_full_state(self) -> Dict[str, Any]:
        """Gather full telemetry for Oracle and Dashboard."""
        rev_state = await self.revenue.get_current_state()
        wallet_assets = await self.wallet.get_balance()

        return {
            "agents_active": len(self.agents),
            "revenue": rev_state.model_dump(),
            "wallet": [a.model_dump() for a in wallet_assets],
            "pheromone_density": 0.45,
            "knowledge_nodes": len(self.graph.nodes),
            "oracle_status": "AWAKE"
        }

if __name__ == "__main__":
    system = SovereignOmega()
    asyncio.run(system.boot())
