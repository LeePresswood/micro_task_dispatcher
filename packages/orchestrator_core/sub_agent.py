from abc import ABC, abstractmethod

class SubAgent(ABC):
    """
    Abstract base class for all Sub-Agents (Mid-Level Agents).
    A Sub-Agent is responsible for a specific domain (e.g., Social Media)
    and manages its own set of micro-tools.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the sub-agent (e.g., 'SocialManager')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what this sub-agent does (for the Orchestrator)."""
        pass

    @abstractmethod
    def run(self, request: str) -> str:
        """
        Executes the sub-agent with the given request.
        Returns a summary of the result.
        """
        pass
