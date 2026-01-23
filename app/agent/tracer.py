"""
Agent execution tracer for observability.

Produces detailed traces of agent execution for debugging,
demonstration, and evaluation purposes.
"""

from datetime import datetime
from typing import List, Optional

from app.agent.types import (
    AgentState,
    AgentTrace,
    StateTransition,
    ToolCall,
    LLMCall,
)


class AgentTracer:
    """
    Records and formats agent execution traces.

    Tracks state transitions, tool calls, and LLM calls
    to produce comprehensive execution logs.
    """

    def __init__(self):
        self.transitions: List[StateTransition] = []
        self.start_time: Optional[datetime] = None
        self.request_id: Optional[str] = None
        self.original_query: Optional[str] = None

        # Current transition accumulators
        self._current_tools: List[ToolCall] = []
        self._current_llm: List[LLMCall] = []
        self._transition_start: Optional[datetime] = None
        self._current_from_state: Optional[AgentState] = None

    def start(self, request_id: str, query: str) -> None:
        """
        Start tracing a new agent run.

        Args:
            request_id: Unique identifier for this run.
            query: Original user query.
        """
        self.transitions = []
        self.start_time = datetime.now()
        self.request_id = request_id
        self.original_query = query
        self._current_tools = []
        self._current_llm = []

    def begin_state(self, state: AgentState) -> None:
        """
        Mark the beginning of a state execution.

        Args:
            state: State being entered.
        """
        self._transition_start = datetime.now()
        self._current_from_state = state
        self._current_tools = []
        self._current_llm = []

    def record_tool_call(self, call: ToolCall) -> None:
        """
        Record a tool call in the current state.

        Args:
            call: ToolCall record to add.
        """
        self._current_tools.append(call)

    def record_tool_calls(self, calls: List[ToolCall]) -> None:
        """
        Record multiple tool calls.

        Args:
            calls: List of ToolCall records.
        """
        self._current_tools.extend(calls)

    def record_llm_call(self, call: LLMCall) -> None:
        """
        Record an LLM call in the current state.

        Args:
            call: LLMCall record to add.
        """
        self._current_llm.append(call)

    def record_llm_calls(self, calls: List[LLMCall]) -> None:
        """
        Record multiple LLM calls.

        Args:
            calls: List of LLMCall records.
        """
        self._current_llm.extend(calls)

    def end_state(
        self,
        to_state: AgentState,
        artifacts: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> None:
        """
        Mark the end of a state execution and record transition.

        Args:
            to_state: State being transitioned to.
            artifacts: List of artifact names produced.
            notes: Optional notes about the transition.
        """
        if self._transition_start is None or self._current_from_state is None:
            return

        duration_ms = (datetime.now() - self._transition_start).total_seconds() * 1000

        transition = StateTransition(
            from_state=self._current_from_state,
            to_state=to_state,
            timestamp=datetime.now(),
            duration_ms=duration_ms,
            tool_calls=self._current_tools.copy(),
            llm_calls=self._current_llm.copy(),
            artifacts_produced=artifacts or [],
            notes=notes
        )

        self.transitions.append(transition)

        # Reset accumulators
        self._current_tools = []
        self._current_llm = []
        self._transition_start = None
        self._current_from_state = None

    def finalize(
        self,
        final_state: AgentState,
        success: bool,
        error: Optional[str] = None
    ) -> AgentTrace:
        """
        Finalize and return the complete trace.

        Args:
            final_state: Terminal state reached.
            success: Whether the run was successful.
            error: Error message if failed.

        Returns:
            Complete AgentTrace object.
        """
        return AgentTrace(
            request_id=self.request_id or "unknown",
            original_query=self.original_query or "",
            start_time=self.start_time or datetime.now(),
            end_time=datetime.now(),
            final_state=final_state,
            transitions=self.transitions,
            success=success,
            error=error
        )

    def format_human_readable(self, trace: AgentTrace) -> str:
        """
        Format trace as human-readable string.

        Args:
            trace: AgentTrace to format.

        Returns:
            Formatted string suitable for logging or display.
        """
        lines = []
        separator = "=" * 65

        # Header
        lines.append(separator)
        lines.append(f"AGENT TRACE: {trace.request_id}")
        lines.append(f'Query: "{trace.original_query}"')
        lines.append(separator)
        lines.append("")

        # Transitions
        elapsed_ms = 0
        for transition in trace.transitions:
            timestamp = f"[{elapsed_ms/1000:07.3f}]"
            elapsed_ms += transition.duration_ms

            lines.append(f"{timestamp} STATE: {transition.from_state.name}")

            # Tool calls
            for tool_call in transition.tool_calls:
                status = "OK" if tool_call.success else "FAIL"
                lines.append(f"            Tool: {tool_call.tool_name}({self._format_args(tool_call.arguments)})")
                lines.append(f"            -> {status} ({tool_call.duration_ms:.0f}ms)")

            # LLM calls
            for llm_call in transition.llm_calls:
                lines.append(f"            LLM: {llm_call.prompt_summary}")
                lines.append(f"            -> {llm_call.tokens} tokens")

            # Artifacts
            if transition.artifacts_produced:
                lines.append(f"            Produced: {', '.join(transition.artifacts_produced)}")

            # Notes
            if transition.notes:
                lines.append(f"            Note: {transition.notes}")

            lines.append(f"            Duration: {transition.duration_ms:.0f}ms")
            lines.append("")

        # Summary
        lines.append(separator)
        lines.append("SUMMARY")
        lines.append(separator)
        lines.append(f"Total duration: {trace.total_duration_ms:.0f}ms")
        lines.append(f"States visited: {' -> '.join(s.name for s in trace.states_visited)}")
        lines.append(f"Total tokens: {trace.total_tokens}")
        lines.append(f"Total tool calls: {trace.total_tool_calls}")
        lines.append(f"Result: {'SUCCESS' if trace.success else 'FAILED'}")

        if trace.error:
            lines.append(f"Error: {trace.error}")

        lines.append(separator)

        return "\n".join(lines)

    def _format_args(self, args: dict) -> str:
        """Format arguments dictionary for display."""
        parts = []
        for key, value in args.items():
            if isinstance(value, str) and len(value) > 30:
                value = value[:27] + "..."
            parts.append(f"{key}={repr(value)}")
        return ", ".join(parts)
