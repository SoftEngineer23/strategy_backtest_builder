"""
Base interface for state handlers.

Each state in the agent workflow implements this interface,
providing consistent execution and validation patterns.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List

from app.agent.types import AgentContext, AgentState, ToolCall, LLMCall


class StateHandler(ABC):
    """
    Abstract base class for all state handlers.

    Each state handler is responsible for:
    1. Validating that required data exists in context
    2. Executing state-specific logic
    3. Updating context with new artifacts
    4. Determining the next state
    """

    @property
    @abstractmethod
    def state(self) -> AgentState:
        """The state this handler manages."""
        pass

    @abstractmethod
    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Execute the state's logic.

        Args:
            context: Current agent context with accumulated artifacts.

        Returns:
            Tuple of (updated context, next state).
        """
        pass

    @abstractmethod
    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate that context has required data for this state.

        Args:
            context: Current agent context.

        Returns:
            True if context is valid for this state, False otherwise.
        """
        pass

    def get_tool_calls(self) -> List[ToolCall]:
        """
        Return tool calls made during last execution.

        Subclasses should track tool calls and return them here
        for tracing purposes.
        """
        return []

    def get_llm_calls(self) -> List[LLMCall]:
        """
        Return LLM calls made during last execution.

        Subclasses should track LLM calls and return them here
        for tracing purposes.
        """
        return []
