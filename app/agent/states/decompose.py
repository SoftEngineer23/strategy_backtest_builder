"""
DECOMPOSE state handler.

Parses the user's natural language request into structured components
that guide subsequent research and synthesis phases.
"""

import json
import re
from typing import List, Tuple, Optional

import anthropic

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    DecomposedRequest,
    Constraint,
    LLMCall,
)
from app.agent.prompts import get_decompose_prompt


class DecomposeHandler(StateHandler):
    """
    Parse user request into structured components.

    This is the entry point of the agent workflow. It analyzes
    the user's natural language request and extracts:
    - Strategy type and characteristics
    - Requested indicators and instruments
    - Constraints and requirements
    - Research queries for the next phase
    """

    def __init__(self, anthropic_client: anthropic.Anthropic, model: str = 'claude-sonnet-4-20250514'):
        """
        Initialize with Anthropic client.

        Args:
            anthropic_client: Configured Anthropic client.
            model: Model identifier to use.
        """
        self.client = anthropic_client
        self.model = model
        self._llm_calls: List[LLMCall] = []

    @property
    def state(self) -> AgentState:
        return AgentState.DECOMPOSE

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for DECOMPOSE state.

        Only requirement is that we have an original query.
        """
        return bool(context.original_query and context.original_query.strip())

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Decompose the user's request.

        Args:
            context: Agent context with original_query.

        Returns:
            Updated context with decomposed_request, next state.
        """
        self._llm_calls = []

        try:
            decomposed = self._decompose_query(context.original_query)
            context.decomposed_request = decomposed

            return context, AgentState.RESEARCH

        except Exception as e:
            context.errors.append(f"Decomposition failed: {str(e)}")
            return context, AgentState.FAILED

    def _decompose_query(self, query: str) -> DecomposedRequest:
        """
        Use LLM to parse the query into components.

        Args:
            query: User's natural language request.

        Returns:
            Structured DecomposedRequest.

        Raises:
            ValueError: If LLM response cannot be parsed.
        """
        prompt = get_decompose_prompt().format(query=query)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.content[0].text

        # Record LLM call
        self._llm_calls.append(LLMCall(
            prompt_summary=f"Decompose: {query[:50]}...",
            response_summary=f"Parsed into structured request",
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            duration_ms=0,
            model=self.model
        ))

        return self._parse_response(raw_text)

    def _parse_response(self, raw_text: str) -> DecomposedRequest:
        """
        Parse LLM response into DecomposedRequest.

        Args:
            raw_text: Raw LLM response.

        Returns:
            Parsed DecomposedRequest.

        Raises:
            ValueError: If JSON parsing fails.
        """
        # Strip markdown code blocks if present
        cleaned_text = re.sub(r'```json\s*\n?', '', raw_text)
        cleaned_text = re.sub(r'```\s*\n?', '', cleaned_text)

        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', cleaned_text)
        if not json_match:
            raise ValueError("No JSON object found in LLM response")

        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

        # Parse constraints
        constraints = None
        if data.get('constraints'):
            constraints = [
                Constraint(name=c['name'], value=c['value'])
                for c in data['constraints']
            ]

        return DecomposedRequest(
            strategy_type=data.get('strategy_type'),
            instruments=data.get('instruments'),
            timeframe=data.get('timeframe'),
            indicators=data.get('indicators'),
            constraints=constraints,
            entry_requirements=data.get('entry_requirements'),
            exit_requirements=data.get('exit_requirements'),
            additional_context=data.get('additional_context'),
            research_queries=data.get('research_queries', [])
        )

    def get_llm_calls(self) -> List[LLMCall]:
        """Return LLM calls made during execution."""
        return self._llm_calls
