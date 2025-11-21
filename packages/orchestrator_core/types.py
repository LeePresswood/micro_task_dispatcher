from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ToolCall:
    """Represents a planned call to a specific tool."""
    tool_name: str
    arguments: Dict[str, Any]
