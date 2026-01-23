"""
COMPLETE state handler.

Packages the validated draft strategy into the final output format.
"""

from typing import List, Tuple

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    FinalStrategy,
    ToolCall,
    LLMCall,
)


class CompleteHandler(StateHandler):
    """
    Package the final validated strategy.

    This is a terminal state that converts the draft strategy
    into the final output format with any accumulated warnings.
    """

    @property
    def state(self) -> AgentState:
        return AgentState.COMPLETE

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for COMPLETE state.

        Requires draft_strategy to package.
        """
        return context.draft_strategy is not None

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Package the final strategy.

        Args:
            context: Agent context with validated draft.

        Returns:
            Updated context with final_strategy, terminal state.
        """
        try:
            draft = context.draft_strategy

            # Build warnings list
            warnings = list(context.warnings)

            # Add warning if critique didn't fully pass
            if context.critique_result and not context.critique_result.overall_pass:
                warnings.append(
                    "Strategy did not fully pass quality criteria. "
                    "Review the following areas: " +
                    ", ".join(context.critique_result.get_failed_criteria())
                )

            # Build metadata
            metadata = {
                'iterations': context.iteration_count,
                'documents_used': (
                    context.research_findings.total_documents
                    if context.research_findings else 0
                ),
                'revision_notes': draft.revision_notes,
            }

            # Package final strategy
            final = FinalStrategy(
                name=draft.name,
                description=draft.description,
                strategy_type=draft.strategy_type,
                entry_rules=draft.entry_rules,
                exit_rules=draft.exit_rules,
                risk_management=draft.risk_management,
                code=draft.code or self._generate_placeholder_code(draft),
                instruments=draft.instruments,
                timeframe=draft.timeframe,
                warnings=warnings,
                metadata=metadata
            )

            context.final_strategy = final
            return context, AgentState.COMPLETE

        except Exception as e:
            context.errors.append(f"Completion failed: {str(e)}")
            return context, AgentState.FAILED

    def _generate_placeholder_code(self, draft) -> str:
        """
        Generate placeholder code if none was provided.

        Args:
            draft: Draft strategy.

        Returns:
            Basic strategy function code.
        """
        entry_comment = "\n    ".join(f"# - {r}" for r in draft.entry_rules[:3])
        exit_comment = "\n    ".join(f"# - {r}" for r in draft.exit_rules[:3])

        return f'''def strategy(df):
    """
    {draft.name}

    Entry Rules:
    {entry_comment}

    Exit Rules:
    {exit_comment}
    """
    import pandas as pd

    signals = pd.Series(0, index=df.index)

    # TODO: Implement strategy logic based on rules above
    # This is a placeholder - actual implementation needed

    return signals
'''

    def get_tool_calls(self) -> List[ToolCall]:
        """No tool calls in COMPLETE state."""
        return []

    def get_llm_calls(self) -> List[LLMCall]:
        """No LLM calls in COMPLETE state."""
        return []
