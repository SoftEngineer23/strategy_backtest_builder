"""
Prompt management for the agent system.

Loads prompts from external text files for easy iteration
and maintenance without code changes.
"""

from pathlib import Path
from functools import lru_cache


PROMPTS_DIR = Path(__file__).parent


@lru_cache(maxsize=10)
def load_prompt(name: str) -> str:
    """
    Load a prompt template from file.

    Args:
        name: Prompt name (without .txt extension).

    Returns:
        Prompt template string.

    Raises:
        FileNotFoundError: If prompt file does not exist.
    """
    prompt_path = PROMPTS_DIR / f"{name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding='utf-8')


def get_decompose_prompt() -> str:
    """Load the decompose state prompt."""
    return load_prompt('decompose')


def get_synthesize_prompt() -> str:
    """Load the synthesize/draft state prompt."""
    return load_prompt('synthesize')


def get_critique_prompt() -> str:
    """Load the critique state prompt."""
    return load_prompt('critique')


def get_refine_prompt() -> str:
    """Load the refine state prompt."""
    return load_prompt('refine')
