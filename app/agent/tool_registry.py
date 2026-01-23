"""
Tool registry for managing and executing agent tools.

The registry provides a central point for tool registration,
discovery, and execution with consistent error handling.
"""

from typing import Any, Dict, List, Optional

from app.agent.tools.base import BaseTool, ToolSchema
from app.agent.types import ToolCall


class ToolRegistry:
    """
    Central registry for agent tools.

    Manages tool registration, lookup, and execution.
    Ensures all tool calls are properly recorded for tracing.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """
        Register a tool with the registry.

        Args:
            tool: Tool instance to register.

        Raises:
            ValueError: If tool with same name already registered.
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.

        Args:
            name: Tool name to look up.

        Returns:
            Tool instance or None if not found.
        """
        return self._tools.get(name)

    def execute(self, name: str, **kwargs) -> ToolCall:
        """
        Execute a tool by name with given arguments.

        Args:
            name: Tool name to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            ToolCall record with result and metadata.

        Raises:
            KeyError: If tool not found.
        """
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Tool not found: {name}")

        # Validate parameters
        validation_error = tool.validate_params(**kwargs)
        if validation_error:
            return ToolCall(
                tool_name=name,
                arguments=kwargs,
                result=None,
                duration_ms=0,
                success=False,
                error=validation_error
            )

        return tool.execute(**kwargs)

    def list_tools(self) -> List[str]:
        """Return list of registered tool names."""
        return list(self._tools.keys())

    def get_schemas(self) -> List[ToolSchema]:
        """Return schemas for all registered tools."""
        return [tool.schema for tool in self._tools.values()]

    def __contains__(self, name: str) -> bool:
        """Check if tool is registered."""
        return name in self._tools

    def __len__(self) -> int:
        """Number of registered tools."""
        return len(self._tools)
