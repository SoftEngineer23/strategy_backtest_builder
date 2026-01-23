"""
Base interfaces and utilities for agent tools.

Tools are the mechanism by which the agent interacts with external services
(RAG, LLM, databases) in a structured, observable way.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time

from app.agent.types import ToolCall


@dataclass
class ToolSchema:
    """
    JSON Schema-style definition of a tool's parameters.

    Used for documentation, validation, and potential future
    integration with LLM function calling.
    """
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters,
            'required': self.required,
        }


class BaseTool(ABC):
    """
    Abstract base class for all agent tools.

    Provides consistent interface for execution, timing,
    and error handling across all tool implementations.
    """

    @property
    @abstractmethod
    def schema(self) -> ToolSchema:
        """Return the tool's schema definition."""
        pass

    @property
    def name(self) -> str:
        """Tool name from schema."""
        return self.schema.name

    @property
    def description(self) -> str:
        """Tool description from schema."""
        return self.schema.description

    @abstractmethod
    def _execute(self, **kwargs) -> Any:
        """
        Internal execution logic. Subclasses implement this.

        Args:
            **kwargs: Tool-specific parameters.

        Returns:
            Tool-specific result.

        Raises:
            Exception: On execution failure.
        """
        pass

    def execute(self, **kwargs) -> ToolCall:
        """
        Execute the tool with timing and error handling.

        Wraps _execute() to provide consistent ToolCall records
        regardless of success or failure.

        Args:
            **kwargs: Tool-specific parameters.

        Returns:
            ToolCall record with result, timing, and status.
        """
        start_time = time.time()

        try:
            result = self._execute(**kwargs)
            duration_ms = (time.time() - start_time) * 1000

            return ToolCall(
                tool_name=self.name,
                arguments=kwargs,
                result=result,
                duration_ms=duration_ms,
                success=True,
                error=None
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            return ToolCall(
                tool_name=self.name,
                arguments=kwargs,
                result=None,
                duration_ms=duration_ms,
                success=False,
                error=str(e)
            )

    def validate_params(self, **kwargs) -> Optional[str]:
        """
        Validate parameters against schema.

        Args:
            **kwargs: Parameters to validate.

        Returns:
            Error message if validation fails, None if valid.
        """
        for param in self.schema.required:
            if param not in kwargs or kwargs[param] is None:
                return f"Missing required parameter: {param}"
        return None
