import asyncio
from typing import List, Dict, Any, Optional
import networkx as nx
import structlog
from pydantic import BaseModel
from core.sovereign_bus.sovereign_bus import SovereignBus
from core.cognitive_plasma.cognitive_plasma import CognitivePlasma
from agents.archetypes.base_agent import SovereignAgent, AgentRole

logger = structlog.get_logger(__name__)

class MorphicTopologyManager:
    """
    Manages the living agent network topology.
    Handles dynamic lifecycle: SPAWN, MERGE, DISSOLVE.
    """
    def __init__(self, bus: SovereignBus, plasma: CognitivePlasma):
        self.bus = bus
        self.plasma = plasma
        self.agents: Dict[str, SovereignAgent] = {}
        self.topology_graph = nx.DiGraph()
        logger.info("MorphicTopologyManager: Initialized")

    async def spawn_agent(self, role: AgentRole) -> SovereignAgent:
        """Create and register a new agent archetype."""
        new_agent = SovereignAgent(role=role)
        self.agents[new_agent.agent_id] = new_agent
        self.topology_graph.add_node(new_agent.agent_id, role=role.value)
        logger.info("Topology: Agent Spawned", id=new_agent.agent_id, role=role.value)
        return new_agent

    async def merge_agents(self, id_a: str, id_b: str, task: str) -> SovereignAgent:
        """Create a Phantom agent from the state fusion of two parents."""
        parent_a = self.agents[id_a]
        parent_b = self.agents[id_b]

        fused_plasma = await self.plasma.merge(parent_a.working_memory, parent_b.working_memory, task)
        fused_memory = self.plasma.deproject(fused_plasma)

        phantom = SovereignAgent(
            role=AgentRole.PHANTOM,
            working_memory=fused_memory
        )
        self.agents[phantom.agent_id] = phantom
        self.topology_graph.add_edge(id_a, phantom.agent_id, type="parent")
        self.topology_graph.add_edge(id_b, phantom.agent_id, type="parent")

        logger.info("Topology: Agents Merged", phantom=phantom.agent_id)
        return phantom

    async def dissolve_agent(self, agent_id: str):
        """Cleanup agent and consolidate its state."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.topology_graph.remove_node(agent_id)
            logger.info("Topology: Agent Dissolved", id=agent_id)
