"""
REFINE state handler.

Addresses issues identified in the critique and produces
an improved draft strategy.
"""

import json
import re
import time
from typing import List, Tuple

import anthropic

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    DraftStrategy,
    StrategyComponent,
    ToolCall,
    LLMCall,
)
from app.agent.tools import RetrieveTool
from app.agent.prompts import get_refine_prompt


class RefineHandler(StateHandler):
    """
    Address critique issues and improve the strategy.

    Uses LLM to refine the draft strategy based on critique
    feedback, potentially fetching additional research.
    """

    def __init__(
        self,
        anthropic_client: anthropic.Anthropic,
        retrieve_tool: RetrieveTool,
        model: str = 'claude-sonnet-4-20250514'
    ):
        """
        Initialize with Anthropic client and retrieve tool.

        Args:
            anthropic_client: Configured Anthropic client.
            retrieve_tool: Tool for additional research if needed.
            model: Model identifier to use.
        """
        self.client = anthropic_client
        self.retrieve_tool = retrieve_tool
        self.model = model
        self._tool_calls: List[ToolCall] = []
        self._llm_calls: List[LLMCall] = []

    @property
    def state(self) -> AgentState:
        return AgentState.REFINE

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for REFINE state.

        Requires draft_strategy and critique_result.
        """
        if not context.draft_strategy:
            return False
        if not context.critique_result:
            return False
        return True

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Refine the draft strategy.

        Args:
            context: Agent context with draft and critique.

        Returns:
            Updated context with refined draft, next state.
        """
        self._tool_calls = []
        self._llm_calls = []

        try:
            # Increment iteration count
            context.iteration_count += 1

            # Gather additional research if needed
            additional_context = self._gather_additional_research(context)

            # Refine the strategy
            refined = self._refine_strategy(context, additional_context)

            # Update draft with refinements
            context.draft_strategy = refined

            return context, AgentState.CRITIQUE

        except Exception as e:
            context.errors.append(f"Refinement failed: {str(e)}")
            return context, AgentState.FAILED

    def _gather_additional_research(self, context: AgentContext) -> str:
        """
        Fetch additional research based on critique gaps.

        Args:
            context: Agent context with critique result.

        Returns:
            Additional context string, or empty if not needed.
        """
        critique = context.critique_result
        if not critique.refinement_instructions:
            return ""

        # Search for content related to refinement needs
        instructions = critique.refinement_instructions.lower()

        # Identify what kind of research might help
        search_query = None
        if 'drawdown' in instructions or 'risk' in instructions:
            search_query = "position sizing drawdown risk management"
        elif 'stop loss' in instructions:
            search_query = "stop loss protected swing invalidation"
        elif 'entry' in instructions:
            search_query = "entry rules confirmation signals"
        elif 'exit' in instructions:
            search_query = "exit rules profit target"

        if search_query:
            result = self.retrieve_tool.execute(
                query=search_query,
                category='all',
                top_k=3
            )
            self._tool_calls.append(result)

            if result.success and result.result:
                docs = result.result
                context_parts = ["## Additional Research\n"]
                for doc in docs:
                    context_parts.append(f"### {doc.title}\n")
                    # Take first 500 chars of each doc
                    context_parts.append(doc.content[:500] + "...\n\n")
                return "\n".join(context_parts)

        return ""

    def _refine_strategy(
        self,
        context: AgentContext,
        additional_context: str
    ) -> DraftStrategy:
        """
        Use LLM to refine the strategy.

        Args:
            context: Agent context with draft and critique.
            additional_context: Additional research context.

        Returns:
            Refined DraftStrategy.
        """
        critique = context.critique_result
        draft = context.draft_strategy

        # Build focus areas from failed criteria
        failed_criteria = critique.get_failed_criteria()
        focus_areas = "\n".join(f"- {c}" for c in failed_criteria) or "- General improvements"

        # Build critique feedback summary
        feedback_parts = []
        for name, evaluation in critique.evaluations.items():
            if evaluation.status.value in ('FAIL', 'PARTIAL'):
                feedback_parts.append(f"- {name}: {evaluation.notes}")
        critique_feedback = "\n".join(feedback_parts) or "No specific failures noted."

        prompt = get_refine_prompt().format(
            original_query=context.original_query,
            draft_strategy=draft.to_prompt_text(),
            critique_feedback=critique_feedback,
            refinement_instructions=critique.refinement_instructions or "Improve overall quality.",
            additional_context=additional_context or "No additional research available.",
            focus_areas=focus_areas,
            strategy_type=draft.strategy_type
        )

        start = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4500,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        duration_ms = (time.time() - start) * 1000

        raw_text = response.content[0].text

        # Record LLM call
        self._llm_calls.append(LLMCall(
            prompt_summary=f"Refine iteration {context.iteration_count}",
            response_summary=f"Refined strategy with {len(raw_text)} chars",
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            duration_ms=duration_ms,
            model=self.model
        ))

        return self._parse_response(raw_text, draft)

    def _parse_response(self, raw_text: str, original_draft: DraftStrategy) -> DraftStrategy:
        """
        Parse LLM response into updated DraftStrategy.

        Args:
            raw_text: Raw LLM response.
            original_draft: Original draft for fallback values.

        Returns:
            Updated DraftStrategy.
        """
        # Strip markdown code blocks if present
        cleaned_text = raw_text
        # Remove opening ```json or ``` markers
        cleaned_text = re.sub(r'```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'```\s*\n?', '', cleaned_text)

        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', cleaned_text)
        if not json_match:
            raise ValueError(f"No JSON object found in LLM response: {raw_text[:200]}...")

        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}\nResponse: {raw_text[:200]}...")

        # Build components
        components = []
        if data.get('entry_rules'):
            components.append(StrategyComponent(
                component_type='entry',
                description='Entry logic',
                rules=data['entry_rules'],
                indicators_used=data.get('indicators_used', [])
            ))
        if data.get('exit_rules'):
            components.append(StrategyComponent(
                component_type='exit',
                description='Exit logic',
                rules=data['exit_rules'],
                indicators_used=[]
            ))
        if data.get('risk_management'):
            components.append(StrategyComponent(
                component_type='risk_management',
                description='Risk management',
                rules=data['risk_management'],
                indicators_used=[]
            ))

        # Track changes
        changes = data.get('changes_made', [])
        revision_notes = original_draft.revision_notes + changes

        return DraftStrategy(
            name=data.get('name', original_draft.name),
            description=data.get('description', original_draft.description),
            strategy_type=data.get('strategy_type', original_draft.strategy_type),
            components=components,
            entry_rules=data.get('entry_rules', original_draft.entry_rules),
            exit_rules=data.get('exit_rules', original_draft.exit_rules),
            risk_management=data.get('risk_management', original_draft.risk_management),
            instruments=original_draft.instruments,
            timeframe=original_draft.timeframe,
            code=data.get('code', original_draft.code),
            revision_notes=revision_notes
        )

    def get_tool_calls(self) -> List[ToolCall]:
        """Return tool calls made during execution."""
        return self._tool_calls

    def get_llm_calls(self) -> List[LLMCall]:
        """Return LLM calls made during execution."""
        return self._llm_calls
