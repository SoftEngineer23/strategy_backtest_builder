"""
Critique strategy tool for evaluating draft strategies.

Uses the LLM to evaluate a draft strategy against a quality
rubric and determine if refinement is needed.
"""

import json
import re
import time
from typing import Any, Dict, Optional

import anthropic

from app.agent.tools.base import BaseTool, ToolSchema
from app.agent.types import (
    CritiqueResult,
    CritiqueEvaluation,
    CritiqueStatus,
    DraftStrategy,
    LLMCall,
)
from app.agent.prompts import get_critique_prompt


class CritiqueTool(BaseTool):
    """
    Evaluate a draft strategy against quality criteria.

    Uses LLM to assess whether the strategy meets quality
    standards or needs refinement.
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
        self._last_llm_call: Optional[LLMCall] = None

    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name='critique_strategy',
            description='Evaluate a draft strategy against quality criteria',
            parameters={
                'draft_strategy': {
                    'type': 'object',
                    'description': 'The draft strategy to evaluate'
                },
                'original_request': {
                    'type': 'string',
                    'description': 'Original user request for constraint checking'
                },
                'iteration': {
                    'type': 'integer',
                    'description': 'Current critique iteration number',
                    'default': 1
                }
            },
            required=['draft_strategy', 'original_request']
        )

    @property
    def last_llm_call(self) -> Optional[LLMCall]:
        """Return the last LLM call record for tracing."""
        return self._last_llm_call

    def _execute(
        self,
        draft_strategy: DraftStrategy,
        original_request: str,
        iteration: int = 1
    ) -> CritiqueResult:
        """
        Critique the draft strategy.

        Args:
            draft_strategy: Strategy to evaluate.
            original_request: Original user query.
            iteration: Current iteration number.

        Returns:
            CritiqueResult with evaluations and pass/fail status.

        Raises:
            ValueError: If LLM response cannot be parsed.
        """
        # Build prompt
        prompt = get_critique_prompt().format(
            original_request=original_request,
            draft_strategy=draft_strategy.to_prompt_text()
        )

        # Call LLM with timing
        start = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        duration_ms = (time.time() - start) * 1000

        raw_text = response.content[0].text

        # Record LLM call for tracing
        self._last_llm_call = LLMCall(
            prompt_summary=f"Critique iteration {iteration}",
            response_summary=f"Evaluation with {len(raw_text)} chars",
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            duration_ms=duration_ms,
            model=self.model
        )

        # Parse response
        return self._parse_response(raw_text, iteration)

    def _parse_response(self, raw_text: str, iteration: int) -> CritiqueResult:
        """
        Parse LLM response into CritiqueResult.

        Args:
            raw_text: Raw LLM response text.
            iteration: Current iteration number.

        Returns:
            Parsed CritiqueResult object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        # Strip markdown code blocks if present
        cleaned_text = re.sub(r'```json\s*\n?', '', raw_text)
        cleaned_text = re.sub(r'```\s*\n?', '', cleaned_text)

        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', cleaned_text)
        if not json_match:
            raise ValueError(f"No JSON object found in LLM response: {raw_text[:200]}...")

        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}\nResponse: {raw_text[:200]}...")

        # Parse evaluations
        evaluations = {}
        for criterion, eval_data in data.get('evaluations', {}).items():
            status_str = eval_data.get('status', 'FAIL')

            # Map string to enum
            status_map = {
                'PASS': CritiqueStatus.PASS,
                'PARTIAL': CritiqueStatus.PARTIAL,
                'FAIL': CritiqueStatus.FAIL,
                'N/A': CritiqueStatus.NOT_APPLICABLE,
            }
            status = status_map.get(status_str, CritiqueStatus.FAIL)

            evaluations[criterion] = CritiqueEvaluation(
                criterion=criterion,
                status=status,
                notes=eval_data.get('notes', '')
            )

        # Determine overall pass
        overall_pass = data.get('overall', 'NEEDS_REFINEMENT') == 'PASS'

        return CritiqueResult(
            evaluations=evaluations,
            overall_pass=overall_pass,
            refinement_instructions=data.get('refinement_instructions'),
            iteration=iteration
        )
