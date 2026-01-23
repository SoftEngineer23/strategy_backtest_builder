"""
Draft strategy tool for synthesizing strategies from research.

Uses the LLM to combine research findings into a coherent
trading strategy with entry/exit rules and code.
"""

import json
import re
from typing import Any, Dict, List, Optional

import anthropic

from app.agent.tools.base import BaseTool, ToolSchema
from app.agent.types import (
    DraftStrategy,
    StrategyComponent,
    ResearchFindings,
    DecomposedRequest,
    LLMCall,
)
from app.agent.prompts import get_synthesize_prompt


class DraftTool(BaseTool):
    """
    Generate a draft trading strategy from research findings.

    Combines decomposed request and research documents to
    synthesize a complete strategy with rules and code.
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
            name='draft_strategy',
            description='Generate a draft trading strategy from research findings and user requirements',
            parameters={
                'original_query': {
                    'type': 'string',
                    'description': 'Original user query'
                },
                'decomposed_request': {
                    'type': 'object',
                    'description': 'Parsed user requirements (DecomposedRequest)'
                },
                'research_findings': {
                    'type': 'object',
                    'description': 'Research results (ResearchFindings)'
                }
            },
            required=['original_query', 'decomposed_request', 'research_findings']
        )

    @property
    def last_llm_call(self) -> Optional[LLMCall]:
        """Return the last LLM call record for tracing."""
        return self._last_llm_call

    def _execute(
        self,
        original_query: str,
        decomposed_request: DecomposedRequest,
        research_findings: ResearchFindings
    ) -> DraftStrategy:
        """
        Generate draft strategy using LLM.

        Args:
            original_query: Original user request.
            decomposed_request: Parsed request components.
            research_findings: Retrieved research documents.

        Returns:
            DraftStrategy object with rules and code.

        Raises:
            ValueError: If LLM response cannot be parsed.
        """
        # Format constraints
        constraints_str = "None specified"
        if decomposed_request.constraints:
            constraints_str = ", ".join(
                f"{c.name}: {c.value}" for c in decomposed_request.constraints
            )

        # Build prompt
        prompt = get_synthesize_prompt().format(
            original_query=original_query,
            strategy_type=decomposed_request.strategy_type or "not specified",
            instruments=", ".join(decomposed_request.instruments or ["any"]),
            timeframe=decomposed_request.timeframe or "not specified",
            indicators=", ".join(decomposed_request.indicators or ["any appropriate"]),
            constraints=constraints_str,
            research_context=research_findings.get_context_text(max_chars=6000)
        )

        # Call LLM
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.content[0].text

        # Record LLM call for tracing
        self._last_llm_call = LLMCall(
            prompt_summary=f"Draft strategy for: {original_query[:50]}...",
            response_summary=f"Generated strategy with {len(raw_text)} chars",
            tokens_input=response.usage.input_tokens,
            tokens_output=response.usage.output_tokens,
            duration_ms=0,  # Will be set by tool execution wrapper
            model=self.model
        )

        # Parse response
        return self._parse_response(raw_text, decomposed_request)

    def _parse_response(
        self,
        raw_text: str,
        decomposed_request: DecomposedRequest
    ) -> DraftStrategy:
        """
        Parse LLM response into DraftStrategy.

        Args:
            raw_text: Raw LLM response text.
            decomposed_request: Original request for fallback values.

        Returns:
            Parsed DraftStrategy object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        # Extract JSON from response (may be wrapped in markdown)
        json_match = re.search(r'\{[\s\S]*\}', raw_text)
        if not json_match:
            raise ValueError("No JSON object found in LLM response")

        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

        # Build strategy components
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
                description='Risk management rules',
                rules=data['risk_management'],
                indicators_used=[]
            ))

        return DraftStrategy(
            name=data.get('name', 'Unnamed Strategy'),
            description=data.get('description', ''),
            strategy_type=data.get('strategy_type', decomposed_request.strategy_type or 'unknown'),
            components=components,
            entry_rules=data.get('entry_rules', []),
            exit_rules=data.get('exit_rules', []),
            risk_management=data.get('risk_management', []),
            instruments=decomposed_request.instruments or [],
            timeframe=decomposed_request.timeframe,
            code=data.get('code'),
            revision_notes=[]
        )
