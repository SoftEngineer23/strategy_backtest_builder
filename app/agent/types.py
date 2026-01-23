"""
Type definitions for the agentic workflow system.

This module defines all data structures used throughout the agent pipeline,
organized into logical groups:

    - Enums: State definitions
    - Tool Types: Tool calls and definitions
    - Request Types: Decomposed user requests
    - Research Types: Retrieved documents and findings
    - Strategy Types: Draft and final strategy structures
    - Critique Types: Quality evaluation results
    - Context Types: Agent execution context and results
    - Trace Types: Observability and debugging
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


# =============================================================================
# ENUMS
# =============================================================================

class AgentState(Enum):
    """
    States in the agent workflow state machine.

    The agent progresses through these states in a defined order,
    with possible loops between CRITIQUE and REFINE.
    """
    DECOMPOSE = auto()
    RESEARCH = auto()
    SYNTHESIZE = auto()
    CRITIQUE = auto()
    REFINE = auto()
    COMPLETE = auto()
    FAILED = auto()


class CritiqueStatus(Enum):
    """Evaluation status for individual critique criteria."""
    PASS = "PASS"
    PARTIAL = "PARTIAL"
    FAIL = "FAIL"
    NOT_APPLICABLE = "N/A"


# =============================================================================
# TOOL TYPES
# =============================================================================

@dataclass
class ToolCall:
    """
    Record of a single tool invocation.

    Captures all information needed to understand what the tool did,
    how long it took, and whether it succeeded.
    """
    tool_name: str
    arguments: Dict[str, Any]
    result: Any
    duration_ms: float
    success: bool
    error: Optional[str] = None


@dataclass
class ToolDefinition:
    """
    Schema definition for a tool available to the agent.

    Provides metadata for tool discovery and validation,
    plus the actual handler function.
    """
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema format
    handler: Callable


@dataclass
class LLMCall:
    """
    Record of a single LLM API invocation.

    Tracks token usage and timing for cost monitoring
    and performance analysis.
    """
    prompt_summary: str
    response_summary: str
    tokens_input: int
    tokens_output: int
    duration_ms: float
    model: str = "claude-sonnet-4-20250514"

    @property
    def tokens(self) -> int:
        """Total tokens used in this call."""
        return self.tokens_input + self.tokens_output


# =============================================================================
# REQUEST TYPES
# =============================================================================

@dataclass
class Constraint:
    """
    A user-specified constraint on the strategy.

    Examples: max drawdown, minimum win rate, position limits.
    """
    name: str
    value: str
    constraint_type: Optional[str] = None  # risk, performance, execution


@dataclass
class DecomposedRequest:
    """
    Structured representation of a user's strategy request.

    Produced by the DECOMPOSE state to guide subsequent research
    and synthesis phases.
    """
    strategy_type: Optional[str] = None  # reversal, continuation, breakout, etc.
    instruments: Optional[List[str]] = None
    timeframe: Optional[str] = None  # intraday, daily, weekly
    indicators: Optional[List[str]] = None
    constraints: Optional[List[Constraint]] = None
    entry_requirements: Optional[List[str]] = None
    exit_requirements: Optional[List[str]] = None
    additional_context: Optional[str] = None
    research_queries: List[str] = field(default_factory=list)


# =============================================================================
# RESEARCH TYPES
# =============================================================================

@dataclass
class RetrievedDocument:
    """
    A document retrieved from the knowledge base.

    Contains the content and metadata needed to understand
    the source and relevance of the information.
    """
    doc_id: str
    content: str
    title: str
    category: str  # indicators, price_action
    relevance_score: float
    concepts: Optional[List[str]] = None


@dataclass
class ResearchFindings:
    """
    Aggregated research results from the RESEARCH state.

    Organizes retrieved documents by topic and tracks
    the queries that produced them.
    """
    queries_executed: List[str]
    documents: List[RetrievedDocument]
    indicator_docs: List[RetrievedDocument] = field(default_factory=list)
    price_action_docs: List[RetrievedDocument] = field(default_factory=list)
    gaps_identified: List[str] = field(default_factory=list)

    @property
    def total_documents(self) -> int:
        """Total number of unique documents retrieved."""
        return len(self.documents)

    def get_context_text(self, max_chars: int = 8000) -> str:
        """
        Compile documents into a context string for LLM consumption.

        Args:
            max_chars: Maximum character limit for the context.

        Returns:
            Formatted string containing document contents.
        """
        context_parts = []
        current_length = 0

        for doc in self.documents:
            doc_text = f"## {doc.title}\n{doc.content}\n\n"
            if current_length + len(doc_text) > max_chars:
                break
            context_parts.append(doc_text)
            current_length += len(doc_text)

        return "".join(context_parts)


# =============================================================================
# STRATEGY TYPES
# =============================================================================

@dataclass
class StrategyComponent:
    """
    A discrete component of a trading strategy.

    Strategies are composed of entry logic, exit logic,
    filters, and risk management rules.
    """
    component_type: str  # entry, exit, filter, risk_management
    description: str
    rules: List[str]
    indicators_used: List[str] = field(default_factory=list)


@dataclass
class DraftStrategy:
    """
    A draft strategy produced by the SYNTHESIZE state.

    Contains both human-readable description and
    structured components for validation.
    """
    name: str
    description: str
    strategy_type: str
    components: List[StrategyComponent]
    entry_rules: List[str]
    exit_rules: List[str]
    risk_management: List[str]
    instruments: List[str] = field(default_factory=list)
    timeframe: Optional[str] = None
    code: Optional[str] = None  # Generated Python code
    revision_notes: List[str] = field(default_factory=list)

    def to_prompt_text(self) -> str:
        """Format strategy for LLM critique prompt."""
        sections = [
            f"Strategy Name: {self.name}",
            f"Type: {self.strategy_type}",
            f"Description: {self.description}",
            "",
            "Entry Rules:",
            *[f"  - {rule}" for rule in self.entry_rules],
            "",
            "Exit Rules:",
            *[f"  - {rule}" for rule in self.exit_rules],
            "",
            "Risk Management:",
            *[f"  - {rule}" for rule in self.risk_management],
        ]
        return "\n".join(sections)


# =============================================================================
# CRITIQUE TYPES
# =============================================================================

@dataclass
class CritiqueEvaluation:
    """Evaluation result for a single critique criterion."""
    criterion: str
    status: CritiqueStatus
    notes: str


@dataclass
class CritiqueResult:
    """
    Complete critique of a draft strategy.

    Produced by the CRITIQUE state, determines whether
    the strategy needs refinement or is ready for completion.
    """
    evaluations: Dict[str, CritiqueEvaluation]
    overall_pass: bool
    refinement_instructions: Optional[str] = None
    iteration: int = 1

    @property
    def needs_refinement(self) -> bool:
        """Whether the strategy requires another refinement pass."""
        return not self.overall_pass

    def get_failed_criteria(self) -> List[str]:
        """Return list of criteria that did not pass."""
        return [
            name for name, eval in self.evaluations.items()
            if eval.status in (CritiqueStatus.FAIL, CritiqueStatus.PARTIAL)
        ]


# =============================================================================
# FINAL OUTPUT TYPES
# =============================================================================

@dataclass
class FinalStrategy:
    """
    The final, validated strategy ready for execution.

    Produced by the COMPLETE state after passing critique.
    """
    name: str
    description: str
    strategy_type: str
    entry_rules: List[str]
    exit_rules: List[str]
    risk_management: List[str]
    code: str
    instruments: List[str]
    timeframe: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# CONTEXT AND RESULT TYPES
# =============================================================================

@dataclass
class AgentContext:
    """
    Execution context passed through all agent states.

    Accumulates artifacts from each state and tracks
    the overall progress of the workflow.
    """
    request_id: str
    original_query: str
    current_state: AgentState
    iteration_count: int = 0
    max_iterations: int = 2

    # Artifacts from each state
    decomposed_request: Optional[DecomposedRequest] = None
    research_findings: Optional[ResearchFindings] = None
    draft_strategy: Optional[DraftStrategy] = None
    critique_result: Optional[CritiqueResult] = None
    final_strategy: Optional[FinalStrategy] = None

    # Tracking
    state_history: List['StateTransition'] = field(default_factory=list)
    total_tokens: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def can_continue(self) -> bool:
        """Check if agent should continue processing."""
        # FAILED is always terminal
        if self.current_state == AgentState.FAILED:
            return False
        # COMPLETE is terminal only after CompleteHandler sets final_strategy
        if self.current_state == AgentState.COMPLETE and self.final_strategy is not None:
            return False
        # Safety limit on iterations (prevents infinite loops in REFINE)
        if self.iteration_count >= self.max_iterations + 1:
            return False
        return True


@dataclass
class AgentResult:
    """
    Final result returned by the agent.

    Contains the strategy (if successful), execution trace,
    and any warnings or errors encountered.
    """
    success: bool
    strategy: Optional[FinalStrategy]
    trace: 'AgentTrace'
    partial_results: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# =============================================================================
# TRACE TYPES
# =============================================================================

@dataclass
class StateTransition:
    """
    Record of a single state transition.

    Captures timing, tool calls, and artifacts for debugging
    and demonstration purposes.
    """
    from_state: AgentState
    to_state: AgentState
    timestamp: datetime
    duration_ms: float
    tool_calls: List[ToolCall] = field(default_factory=list)
    llm_calls: List[LLMCall] = field(default_factory=list)
    artifacts_produced: List[str] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class AgentTrace:
    """
    Complete execution trace for an agent run.

    Provides full visibility into agent behavior for
    debugging, demonstration, and evaluation.
    """
    request_id: str
    original_query: str
    start_time: datetime
    end_time: Optional[datetime] = None
    final_state: Optional[AgentState] = None
    transitions: List[StateTransition] = field(default_factory=list)
    success: bool = False
    error: Optional[str] = None

    @property
    def total_duration_ms(self) -> float:
        """Total execution time in milliseconds."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return sum(t.duration_ms for t in self.transitions)

    @property
    def total_tokens(self) -> int:
        """Total tokens used across all LLM calls."""
        return sum(
            call.tokens
            for transition in self.transitions
            for call in transition.llm_calls
        )

    @property
    def total_tool_calls(self) -> int:
        """Total number of tool invocations."""
        return sum(len(t.tool_calls) for t in self.transitions)

    @property
    def states_visited(self) -> List[AgentState]:
        """Ordered list of states visited during execution."""
        if not self.transitions:
            return []
        states = [self.transitions[0].from_state]
        states.extend(t.to_state for t in self.transitions)
        return states

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary for JSON export."""
        return {
            'request_id': self.request_id,
            'original_query': self.original_query,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_duration_ms': self.total_duration_ms,
            'final_state': self.final_state.name if self.final_state else None,
            'states_visited': [s.name for s in self.states_visited],
            'total_tokens': self.total_tokens,
            'total_tool_calls': self.total_tool_calls,
            'success': self.success,
            'error': self.error,
        }


# =============================================================================
# STATE MACHINE CONSTANTS
# =============================================================================

VALID_TRANSITIONS: Dict[AgentState, List[AgentState]] = {
    AgentState.DECOMPOSE: [AgentState.RESEARCH, AgentState.FAILED],
    AgentState.RESEARCH: [AgentState.SYNTHESIZE, AgentState.FAILED],
    AgentState.SYNTHESIZE: [AgentState.CRITIQUE, AgentState.FAILED],
    AgentState.CRITIQUE: [AgentState.COMPLETE, AgentState.REFINE, AgentState.FAILED],
    AgentState.REFINE: [AgentState.CRITIQUE, AgentState.FAILED],
    AgentState.COMPLETE: [AgentState.COMPLETE],  # Terminal state stays in COMPLETE
    AgentState.FAILED: [AgentState.FAILED],  # Terminal state stays in FAILED
}


def is_valid_transition(from_state: AgentState, to_state: AgentState) -> bool:
    """Check if a state transition is valid according to the state machine."""
    return to_state in VALID_TRANSITIONS.get(from_state, [])
