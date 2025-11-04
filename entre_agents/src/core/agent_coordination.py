"""
Lightweight agent coordination system.

Enables Chief of Staff to invoke specialist agents and coordinate responses.
Built incrementally - only what we need now, not the full framework.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class AgentConsultation:
    """
    Represents a consultation request from one agent to another.
    """
    id: str
    from_agent: str
    to_agent: str
    question: str
    context: Dict[str, Any]
    timestamp: datetime
    response: Optional[str] = None
    response_timestamp: Optional[datetime] = None
    metadata: Optional[Dict] = None


class AgentRegistry:
    """
    Registry of all available agents.
    Enables agents to find and invoke each other.
    """

    def __init__(self):
        self.agents = {}  # agent_name -> agent_instance
        self.agent_capabilities = {}  # agent_name -> capability_description

    def register_agent(self, agent_name: str, agent_instance, capabilities: str):
        """
        Register an agent in the system.

        Args:
            agent_name: Unique agent identifier (e.g., "Chief of Staff")
            agent_instance: The agent object
            capabilities: Description of what this agent can do
        """
        self.agents[agent_name] = agent_instance
        self.agent_capabilities[agent_name] = capabilities
        print(f"✓ Registered agent: {agent_name}")

    def get_agent(self, agent_name: str):
        """Get agent instance by name."""
        return self.agents.get(agent_name)

    def list_agents(self) -> List[Dict[str, str]]:
        """List all available agents and their capabilities."""
        return [
            {
                'name': name,
                'capabilities': self.agent_capabilities[name],
                'status': 'available' if self.agents[name] else 'unavailable'
            }
            for name in self.agents.keys()
        ]

    def get_available_agents_for_llm(self) -> str:
        """
        Format agent list for LLM consumption.
        Returns a description of available agents the Chief can consult.
        """
        agent_list = []
        for name, capabilities in self.agent_capabilities.items():
            if name != "Chief of Staff":  # Don't list self
                agent_list.append(f"- **{name}**: {capabilities}")

        return "Available Specialist Agents:\n" + "\n".join(agent_list)


class AgentCoordinator:
    """
    Coordinates multi-agent consultations.
    Lightweight implementation - just what we need for Chief of Staff to invoke specialists.
    """

    def __init__(self, registry: AgentRegistry, db=None):
        self.registry = registry
        self.db = db
        self.consultation_history = []  # In-memory for now, can persist to DB later

    def consult_agent(
        self,
        from_agent_name: str,
        to_agent_name: str,
        question: str,
        context: Dict[str, Any]
    ) -> AgentConsultation:
        """
        One agent consults another agent.

        Args:
            from_agent_name: Name of agent making the request (usually "Chief of Staff")
            to_agent_name: Name of specialist agent to consult
            question: The question/task for the specialist
            context: Relevant context for the specialist

        Returns:
            AgentConsultation with the specialist's response
        """

        # Create consultation record
        consultation = AgentConsultation(
            id=str(uuid.uuid4()),
            from_agent=from_agent_name,
            to_agent=to_agent_name,
            question=question,
            context=context,
            timestamp=datetime.utcnow()
        )

        # Get the specialist agent
        specialist = self.registry.get_agent(to_agent_name)

        if not specialist:
            consultation.response = f"[ERROR] Agent '{to_agent_name}' not available"
            consultation.metadata = {'error': 'agent_not_found'}
            return consultation

        # Invoke the specialist
        try:
            # Specialists have a consult() method that handles consultation requests
            response = specialist.consult(
                question=question,
                context=context,
                from_agent=from_agent_name
            )

            consultation.response = response
            consultation.response_timestamp = datetime.utcnow()
            consultation.metadata = {
                'success': True,
                'agent_invoked': to_agent_name
            }

        except Exception as e:
            consultation.response = f"[ERROR] {to_agent_name} encountered an error: {str(e)}"
            consultation.metadata = {
                'success': False,
                'error': str(e)
            }

        # Store consultation history
        self.consultation_history.append(consultation)

        # Optionally persist to database
        if self.db:
            self._persist_consultation(consultation)

        return consultation

    def get_consultation_history(
        self,
        agent_name: Optional[str] = None,
        limit: int = 10
    ) -> List[AgentConsultation]:
        """
        Retrieve consultation history.

        Args:
            agent_name: Filter by agent (either from or to)
            limit: Maximum number of consultations to return
        """
        history = self.consultation_history

        if agent_name:
            history = [
                c for c in history
                if c.from_agent == agent_name or c.to_agent == agent_name
            ]

        return history[-limit:]

    def _persist_consultation(self, consultation: AgentConsultation):
        """
        Persist consultation to database for learning/analysis.
        """
        if not self.db:
            return

        self.db.execute(
            """
            INSERT INTO agent_consultations
            (id, from_agent, to_agent, question, context, response,
             timestamp, response_timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                consultation.id,
                consultation.from_agent,
                consultation.to_agent,
                consultation.question,
                str(consultation.context),  # JSON string
                consultation.response,
                consultation.timestamp.isoformat(),
                consultation.response_timestamp.isoformat() if consultation.response_timestamp else None,
                str(consultation.metadata) if consultation.metadata else None
            )
        )
        self.db.commit()


def format_consultation_for_display(consultation: AgentConsultation) -> str:
    """
    Format a consultation for display to the entrepreneur.
    Shows which agent was consulted and their response.
    """
    duration = ""
    if consultation.response_timestamp:
        delta = (consultation.response_timestamp - consultation.timestamp).total_seconds()
        duration = f" ({delta:.1f}s)"

    return f"""
╭─────────────────────────────────────────╮
│ Consulted: {consultation.to_agent}{duration}
╰─────────────────────────────────────────╯

Question: {consultation.question}

Response:
{consultation.response}
"""


# Global registry and coordinator (initialized by app)
agent_registry = AgentRegistry()
agent_coordinator = None  # Initialized with DB in main app
