"""
Agent state handlers module.

Each state in the agent workflow has a dedicated handler that implements
the StateHandler interface, providing consistent execution and validation.

State Flow:
    DECOMPOSE -> RESEARCH -> SYNTHESIZE -> CRITIQUE -> COMPLETE
                                              |
                                              v
                                           REFINE (loops back to CRITIQUE)
"""

from app.agent.states.base import StateHandler
from app.agent.states.decompose import DecomposeHandler
from app.agent.states.research import ResearchHandler
from app.agent.states.synthesize import SynthesizeHandler
from app.agent.states.critique import CritiqueHandler
from app.agent.states.refine import RefineHandler
from app.agent.states.complete import CompleteHandler

__all__ = [
    'StateHandler',
    'DecomposeHandler',
    'ResearchHandler',
    'SynthesizeHandler',
    'CritiqueHandler',
    'RefineHandler',
    'CompleteHandler',
]
