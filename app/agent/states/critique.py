"""
CRITIQUE state handler.

Evaluates the draft strategy against a quality rubric
to determine if refinement is needed.
"""

from typing import List, Tuple

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    ToolCall,
    LLMCall,
)
from app.agent.tools import CritiqueTool


class CritiqueHandler(StateHandler):
    """
    Evaluate draft strategy against quality criteria.

    Uses the CritiqueTool to assess whether the strategy
    meets quality standards or needs refinement.
    """

    def __init__(self, critique_tool: CritiqueTool):
        """
        Initialize with critique tool.

        Args:
            critique_tool: Tool for strategy evaluation.
        """
        self.critique_tool = critique_tool
        self._tool_calls: List[ToolCall] = []
        self._llm_calls: List[LLMCall] = []

    @property
    def state(self) -> AgentState:
        return AgentState.CRITIQUE

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for CRITIQUE state.

        Requires draft_strategy to evaluate.
        """
        return context.draft_strategy is not None

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Critique the draft strategy.

        Args:
            context: Agent context with draft_strategy.

        Returns:
            Updated context with critique_result, next state.
        """
        self._tool_calls = []
        self._llm_calls = []

        try:
            # Determine iteration number
            iteration = context.iteration_count + 1

            result = self.critique_tool.execute(
                draft_strategy=context.draft_strategy,
                original_request=context.original_query,
                iteration=iteration
            )
            self._tool_calls.append(result)

            # Capture LLM call from tool
            if self.critique_tool.last_llm_call:
                self._llm_calls.append(self.critique_tool.last_llm_call)

            if not result.success:
                context.errors.append(f"Critique failed: {result.error}")
                return context, AgentState.FAILED

            context.critique_result = result.result

            # Determine next state based on critique
            if result.result.overall_pass:
                return context, AgentState.COMPLETE
            else:
                # Check if we've exceeded max iterations
                if context.iteration_count >= context.max_iterations:
                    context.warnings.append(
                        f"Max iterations ({context.max_iterations}) reached. "
                        "Returning best available strategy."
                    )
                    return context, AgentState.COMPLETE
                else:
                    return context, AgentState.REFINE

        except Exception as e:
            context.errors.append(f"Critique failed: {str(e)}")
            return context, AgentState.FAILED

    def get_tool_calls(self) -> List[ToolCall]:
        """Return tool calls made during execution."""
        return self._tool_calls

    def get_llm_calls(self) -> List[LLMCall]:
        """Return LLM calls made during execution."""
        return self._llm_calls
