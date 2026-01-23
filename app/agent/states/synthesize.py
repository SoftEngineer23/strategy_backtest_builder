"""
SYNTHESIZE state handler.

Combines research findings into a coherent draft strategy
with entry rules, exit rules, and executable code.
"""

from typing import List, Tuple

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    ToolCall,
    LLMCall,
)
from app.agent.tools import DraftTool


class SynthesizeHandler(StateHandler):
    """
    Combine research into a draft strategy.

    Uses the DraftTool to generate a complete strategy from
    the accumulated research documents and user requirements.
    """

    def __init__(self, draft_tool: DraftTool):
        """
        Initialize with draft tool.

        Args:
            draft_tool: Tool for strategy generation.
        """
        self.draft_tool = draft_tool
        self._tool_calls: List[ToolCall] = []
        self._llm_calls: List[LLMCall] = []

    @property
    def state(self) -> AgentState:
        return AgentState.SYNTHESIZE

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for SYNTHESIZE state.

        Requires decomposed_request and research_findings.
        """
        if not context.decomposed_request:
            return False
        if not context.research_findings:
            return False
        return True

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Generate draft strategy from research.

        Args:
            context: Agent context with research findings.

        Returns:
            Updated context with draft_strategy, next state.
        """
        self._tool_calls = []
        self._llm_calls = []

        try:
            result = self.draft_tool.execute(
                original_query=context.original_query,
                decomposed_request=context.decomposed_request,
                research_findings=context.research_findings
            )
            self._tool_calls.append(result)

            # Capture LLM call from tool
            if self.draft_tool.last_llm_call:
                self._llm_calls.append(self.draft_tool.last_llm_call)

            if not result.success:
                context.errors.append(f"Strategy synthesis failed: {result.error}")
                return context, AgentState.FAILED

            context.draft_strategy = result.result
            return context, AgentState.CRITIQUE

        except Exception as e:
            context.errors.append(f"Synthesis failed: {str(e)}")
            return context, AgentState.FAILED

    def get_tool_calls(self) -> List[ToolCall]:
        """Return tool calls made during execution."""
        return self._tool_calls

    def get_llm_calls(self) -> List[LLMCall]:
        """Return LLM calls made during execution."""
        return self._llm_calls
