"""
Simple tool execution system for agents.

Enables agents to DO things, not just provide advice.
Built incrementally - starting with essential tools.
"""

from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class ToolResult:
    """Result of tool execution."""
    tool_name: str
    success: bool
    result: Any
    error: str = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class Tool:
    """
    Represents a tool that agents can use.
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters_schema: Dict[str, Any]
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters_schema = parameters_schema

    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.
        """
        try:
            result = self.function(**kwargs)
            return ToolResult(
                tool_name=self.name,
                success=True,
                result=result
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                result=None,
                error=str(e)
            )

    def to_anthropic_schema(self) -> Dict:
        """
        Convert tool to Anthropic function calling schema.
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": self.parameters_schema,
                "required": list(self.parameters_schema.keys())
            }
        }


class ToolRegistry:
    """
    Registry of available tools.
    """

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool
        print(f"✓ Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Tool:
        """Get tool by name."""
        return self.tools.get(name)

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name with parameters."""
        tool = self.get_tool(tool_name)

        if not tool:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=f"Tool '{tool_name}' not found"
            )

        return tool.execute(**parameters)

    def get_tools_for_anthropic(self) -> List[Dict]:
        """Get all tools in Anthropic function calling format."""
        return [tool.to_anthropic_schema() for tool in self.tools.values()]

    def list_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self.tools.keys())


# ============================================================================
# BUILT-IN TOOLS
# ============================================================================

def create_document(title: str, content: str, format: str = "markdown") -> Dict[str, str]:
    """
    Create a document and save it to the user's workspace.

    Args:
        title: Document title
        content: Document content
        format: Document format (markdown, txt, etc.)

    Returns:
        Dict with file_path and preview
    """
    import os
    from pathlib import Path
    import re

    # Sanitize filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    filename = f"{safe_title}.{format}"

    # Create documents directory if it doesn't exist
    docs_dir = Path("data/documents")
    docs_dir.mkdir(parents=True, exist_ok=True)

    file_path = docs_dir / filename

    # Write document
    with open(file_path, 'w') as f:
        f.write(content)

    # Create preview (first 200 chars)
    preview = content[:200] + "..." if len(content) > 200 else content

    return {
        "file_path": str(file_path),
        "filename": filename,
        "preview": preview,
        "size_bytes": len(content),
        "format": format
    }


def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Send an email (mock for now, will integrate with real email service later).

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body

    Returns:
        Dict with status and message_id
    """
    # For now, just log it (in production, integrate with SendGrid, etc.)
    print(f"\n📧 EMAIL (Mock):")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print()

    return {
        "status": "sent (mock)",
        "message_id": f"mock_{datetime.utcnow().timestamp()}",
        "to": to,
        "subject": subject,
        "note": "Email not actually sent - mock mode. Will integrate real email service later."
    }


def consult_agent(agent_name: str, question: str) -> str:
    """
    Consult another specialist agent.

    This tool is special - it's dynamically linked to the agent coordination system.
    The actual implementation is injected at runtime.

    Args:
        agent_name: Name of agent to consult
        question: Question for the specialist

    Returns:
        Response from specialist agent
    """
    # This will be replaced with actual coordination call
    return f"[consult_agent tool - needs coordinator injection]"


def search_knowledge_base(query: str, limit: int = 5) -> List[Dict[str, str]]:
    """
    Search the entrepreneur's knowledge base (documents, notes, decisions).

    Args:
        query: Search query
        limit: Maximum number of results

    Returns:
        List of relevant documents/notes
    """
    # Placeholder - in production, this would do semantic search over documents
    return [
        {
            "title": "Example Document",
            "snippet": "This is where search results would appear...",
            "source": "knowledge_base",
            "relevance_score": 0.85
        }
    ]


# ============================================================================
# DEFAULT TOOL REGISTRY
# ============================================================================

def create_default_tools() -> ToolRegistry:
    """
    Create the default tool registry with built-in tools.
    """
    registry = ToolRegistry()

    # Document creation tool
    registry.register_tool(Tool(
        name="create_document",
        description="Create and save a document (markdown, text, etc.) to the workspace",
        function=create_document,
        parameters_schema={
            "title": {
                "type": "string",
                "description": "Title of the document"
            },
            "content": {
                "type": "string",
                "description": "Full content of the document"
            },
            "format": {
                "type": "string",
                "description": "Document format",
                "enum": ["markdown", "txt", "html"]
            }
        }
    ))

    # Email sending tool
    registry.register_tool(Tool(
        name="send_email",
        description="Send an email to someone (currently mock mode)",
        function=send_email,
        parameters_schema={
            "to": {
                "type": "string",
                "description": "Recipient email address"
            },
            "subject": {
                "type": "string",
                "description": "Email subject line"
            },
            "body": {
                "type": "string",
                "description": "Email body content"
            }
        }
    ))

    # Agent consultation tool
    registry.register_tool(Tool(
        name="consult_specialist_agent",
        description="Consult another specialist agent (Market Discovery, Product & Technology, or Capital & Financing) for their expertise",
        function=consult_agent,
        parameters_schema={
            "agent_name": {
                "type": "string",
                "description": "Name of the specialist agent to consult",
                "enum": ["Market Discovery Agent", "Product & Technology Agent", "Capital & Financing Agent"]
            },
            "question": {
                "type": "string",
                "description": "The question or task for the specialist agent"
            }
        }
    ))

    # Knowledge base search
    registry.register_tool(Tool(
        name="search_knowledge_base",
        description="Search the entrepreneur's knowledge base (past decisions, documents, notes) for relevant information",
        function=search_knowledge_base,
        parameters_schema={
            "query": {
                "type": "string",
                "description": "Search query"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return (default 5)"
            }
        }
    ))

    return registry
