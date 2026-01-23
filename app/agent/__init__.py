"""
Agentic workflow module for Strategy Builder.

This module implements a state machine-based agent that decomposes strategy
requests, performs targeted research, synthesizes findings, and refines
output through self-critique.

Architecture:
    - types.py: Data models and type definitions
    - orchestrator.py: State machine execution engine
    - tracer.py: Observability and execution tracing
    - tool_registry.py: Tool management and execution
    - tools/: Individual tool implementations
    - states/: State handler implementations
    - prompts/: LLM prompt templates

State Flow:
    DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE -> COMPLETE
                                              |
                                              v
                                           REFINE (loops back to CRITIQUE)
"""

from app.agent.types import (
    # Enums
    AgentState,
    CritiqueStatus,
    # Tool types
    ToolCall,
    ToolDefinition,
    LLMCall,
    # Request types
    Constraint,
    DecomposedRequest,
    # Research types
    RetrievedDocument,
    ResearchFindings,
    # Strategy types
    StrategyComponent,
    DraftStrategy,
    FinalStrategy,
    # Critique types
    CritiqueEvaluation,
    CritiqueResult,
    # Context types
    AgentContext,
    AgentResult,
    # Trace types
    StateTransition,
    AgentTrace,
    # Constants
    VALID_TRANSITIONS,
    is_valid_transition,
)

__all__ = [
    # Enums
    'AgentState',
    'CritiqueStatus',
    # Tool types
    'ToolCall',
    'ToolDefinition',
    'LLMCall',
    # Request types
    'Constraint',
    'DecomposedRequest',
    # Research types
    'RetrievedDocument',
    'ResearchFindings',
    # Strategy types
    'StrategyComponent',
    'DraftStrategy',
    'FinalStrategy',
    # Critique types
    'CritiqueEvaluation',
    'CritiqueResult',
    # Context types
    'AgentContext',
    'AgentResult',
    # Trace types
    'StateTransition',
    'AgentTrace',
    # Constants
    'VALID_TRANSITIONS',
    'is_valid_transition',
]
