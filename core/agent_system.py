"""
Apollo Agent System (safe skeleton)

A minimal AgentManager to register and track agents. This is a non-executing
framework: it does not run code, spawn processes, or perform autonomous tasks.
It provides a clear surface for future safe implementations and tests.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class AgentDescriptor:
    id: str
    role: str
    description: Optional[str] = None
    active: bool = False


class AgentManager:
    """
    Simple in-memory registry for agent descriptors.
    Designed to be deterministic and testable.
    """

    def __init__(self):
        self._agents: Dict[str, AgentDescriptor] = {}

    def register_agent(self, descriptor: AgentDescriptor) -> bool:
        """Register an agent descriptor. Returns True if added, False if exists."""
        if descriptor.id in self._agents:
            return False
        self._agents[descriptor.id] = descriptor
        return True

    def list_agents(self) -> List[AgentDescriptor]:
        """Return a list of registered agent descriptors."""
        return list(self._agents.values())

    def set_active(self, agent_id: str, active: bool) -> bool:
        """Mark an agent active/inactive. Returns False if agent not found."""
        agent = self._agents.get(agent_id)
        if agent is None:
            return False
        agent.active = active
        return True

    def find_agent(self, agent_id: str) -> Optional[AgentDescriptor]:
        """Retrieve an agent descriptor or None if not found."""
        return self._agents.get(agent_id)
