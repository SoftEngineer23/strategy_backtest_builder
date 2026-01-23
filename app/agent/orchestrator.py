"""
Agent orchestrator - the state machine execution engine.

Coordinates state handlers to process user requests through
the complete agentic workflow.
"""

import uuid
import time
from pathlib import Path
from typing import Dict, Optional

import anthropic

from app.agent.types import (
    AgentState,
    AgentContext,
    AgentResult,
    VALID_TRANSITIONS,
    is_valid_transition,
)
from app.agent.tracer import AgentTracer
from app.agent.states import (
    StateHandler,
    DecomposeHandler,
    ResearchHandler,
    SynthesizeHandler,
    CritiqueHandler,
    RefineHandler,
    CompleteHandler,
)
from app.agent.tools import (
    RetrieveTool,
    IndicatorTool,
    DraftTool,
    CritiqueTool,
)
from app.services.rag_service import RAGService


class StrategyAgent:
    """
    State machine orchestrator for strategy generation.

    Coordinates the flow through DECOMPOSE -> RESEARCH -> SYNTHESIZE ->
    CRITIQUE -> (REFINE ->) COMPLETE, managing state transitions
    and producing execution traces.
    """

    def __init__(
        self,
        anthropic_client: anthropic.Anthropic,
        rag_service: RAGService,
        corpus_dir: Path,
        model: str = 'claude-sonnet-4-20250514',
        max_iterations: int = 2
    ):
        """
        Initialize the agent with required services.

        Args:
            anthropic_client: Configured Anthropic client.
            rag_service: RAG service for document retrieval.
            corpus_dir: Path to corpus directory.
            model: Model identifier for LLM calls.
            max_iterations: Maximum critique/refine iterations.
        """
        self.model = model
        self.max_iterations = max_iterations
        self.tracer = AgentTracer()

        # Initialize tools
        self.retrieve_tool = RetrieveTool(rag_service)
        self.indicator_tool = IndicatorTool(corpus_dir)
        self.draft_tool = DraftTool(anthropic_client, model)
        self.critique_tool = CritiqueTool(anthropic_client, model)

        # Initialize state handlers
        self.handlers: Dict[AgentState, StateHandler] = {
            AgentState.DECOMPOSE: DecomposeHandler(anthropic_client, model),
            AgentState.RESEARCH: ResearchHandler(self.retrieve_tool, self.indicator_tool),
            AgentState.SYNTHESIZE: SynthesizeHandler(self.draft_tool),
            AgentState.CRITIQUE: CritiqueHandler(self.critique_tool),
            AgentState.REFINE: RefineHandler(anthropic_client, self.retrieve_tool, model),
            AgentState.COMPLETE: CompleteHandler(),
        }

    def run(self, query: str) -> AgentResult:
        """
        Execute the agent workflow for a user query.

        Args:
            query: User's natural language strategy request.

        Returns:
            AgentResult with strategy, trace, and status.
        """
        # Initialize context
        request_id = str(uuid.uuid4())[:8]
        context = AgentContext(
            request_id=request_id,
            original_query=query,
            current_state=AgentState.DECOMPOSE,
            iteration_count=0,
            max_iterations=self.max_iterations
        )

        # Start tracing
        self.tracer.start(request_id, query)

        # Run state machine
        while context.can_continue():
            context = self._execute_state(context)

            # FAILED is immediately terminal
            if context.current_state == AgentState.FAILED:
                break

            # COMPLETE is terminal only after CompleteHandler has run
            # (CompleteHandler sets final_strategy, then returns COMPLETE)
            if context.current_state == AgentState.COMPLETE and context.final_strategy is not None:
                break

        # Build result
        success = context.current_state == AgentState.COMPLETE and context.final_strategy is not None
        error = context.errors[-1] if context.errors else None

        trace = self.tracer.finalize(
            final_state=context.current_state,
            success=success,
            error=error
        )

        return AgentResult(
            success=success,
            strategy=context.final_strategy,
            trace=trace,
            partial_results=self._build_partial_results(context),
            warnings=context.warnings,
            errors=context.errors
        )

    def _execute_state(self, context: AgentContext) -> AgentContext:
        """
        Execute the current state's handler.

        Args:
            context: Current agent context.

        Returns:
            Updated context after state execution.
        """
        current_state = context.current_state
        handler = self.handlers.get(current_state)

        if handler is None:
            context.errors.append(f"No handler for state: {current_state}")
            context.current_state = AgentState.FAILED
            return context

        # Begin tracing this state
        self.tracer.begin_state(current_state)

        # Validate entry conditions
        if not handler.validate_entry(context):
            context.errors.append(f"Invalid entry conditions for state: {current_state}")
            self.tracer.end_state(
                AgentState.FAILED,
                notes=f"Validation failed for {current_state.name}"
            )
            context.current_state = AgentState.FAILED
            return context

        # Execute the state
        try:
            context, next_state = handler.execute(context)

            # Validate transition
            if not is_valid_transition(current_state, next_state):
                context.errors.append(
                    f"Invalid transition: {current_state.name} -> {next_state.name}"
                )
                next_state = AgentState.FAILED

            # Record tool and LLM calls from handler
            self.tracer.record_tool_calls(handler.get_tool_calls())
            self.tracer.record_llm_calls(handler.get_llm_calls())

            # Determine artifacts produced
            artifacts = self._get_artifacts_produced(current_state, context)

            # End state trace
            self.tracer.end_state(
                next_state,
                artifacts=artifacts,
                notes=self._get_state_notes(current_state, context)
            )

            context.current_state = next_state
            return context

        except Exception as e:
            context.errors.append(f"State execution error: {str(e)}")
            self.tracer.end_state(
                AgentState.FAILED,
                notes=f"Exception: {str(e)}"
            )
            context.current_state = AgentState.FAILED
            return context

    def _get_artifacts_produced(self, state: AgentState, context: AgentContext) -> list:
        """Determine what artifacts were produced by a state."""
        artifacts = []

        if state == AgentState.DECOMPOSE and context.decomposed_request:
            artifacts.append("decomposed_request")
            if context.decomposed_request.research_queries:
                artifacts.append(f"{len(context.decomposed_request.research_queries)} research queries")

        elif state == AgentState.RESEARCH and context.research_findings:
            artifacts.append("research_findings")
            artifacts.append(f"{context.research_findings.total_documents} documents")

        elif state == AgentState.SYNTHESIZE and context.draft_strategy:
            artifacts.append("draft_strategy")
            if context.draft_strategy.code:
                artifacts.append("strategy code")

        elif state == AgentState.CRITIQUE and context.critique_result:
            artifacts.append("critique_result")
            status = "PASS" if context.critique_result.overall_pass else "NEEDS_REFINEMENT"
            artifacts.append(f"overall: {status}")

        elif state == AgentState.REFINE and context.draft_strategy:
            artifacts.append("refined_strategy")

        elif state == AgentState.COMPLETE and context.final_strategy:
            artifacts.append("final_strategy")

        return artifacts

    def _get_state_notes(self, state: AgentState, context: AgentContext) -> Optional[str]:
        """Generate notes for a state transition."""
        if state == AgentState.DECOMPOSE and context.decomposed_request:
            return f"Strategy type: {context.decomposed_request.strategy_type or 'unspecified'}"

        elif state == AgentState.CRITIQUE and context.critique_result:
            if context.critique_result.overall_pass:
                return "All criteria passed"
            else:
                failed = context.critique_result.get_failed_criteria()
                return f"Failed criteria: {', '.join(failed)}"

        elif state == AgentState.REFINE:
            return f"Iteration {context.iteration_count}"

        return None

    def _build_partial_results(self, context: AgentContext) -> dict:
        """Build partial results dictionary for failed runs."""
        results = {}

        if context.decomposed_request:
            results['decomposed_request'] = {
                'strategy_type': context.decomposed_request.strategy_type,
                'indicators': context.decomposed_request.indicators,
                'constraints': [
                    {'name': c.name, 'value': c.value}
                    for c in (context.decomposed_request.constraints or [])
                ],
            }

        if context.research_findings:
            results['research_summary'] = {
                'total_documents': context.research_findings.total_documents,
                'queries_executed': context.research_findings.queries_executed,
            }

        if context.draft_strategy:
            results['draft_strategy'] = {
                'name': context.draft_strategy.name,
                'entry_rules': context.draft_strategy.entry_rules,
                'exit_rules': context.draft_strategy.exit_rules,
            }

        return results


def create_agent(
    api_key: str,
    chroma_dir: Path,
    corpus_dir: Path,
    model: str = 'claude-sonnet-4-20250514',
    max_iterations: int = 2
) -> StrategyAgent:
    """
    Factory function to create a configured StrategyAgent.

    Args:
        api_key: Anthropic API key.
        chroma_dir: Path to ChromaDB directory.
        corpus_dir: Path to corpus directory.
        model: Model identifier.
        max_iterations: Maximum critique iterations.

    Returns:
        Configured StrategyAgent instance.
    """
    client = anthropic.Anthropic(api_key=api_key)
    rag_service = RAGService(chroma_dir)

    return StrategyAgent(
        anthropic_client=client,
        rag_service=rag_service,
        corpus_dir=corpus_dir,
        model=model,
        max_iterations=max_iterations
    )
