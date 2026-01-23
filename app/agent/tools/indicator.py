"""
Indicator info tool for direct document lookup.

Provides fast, direct access to specific indicator documentation
without semantic search overhead.
"""

from pathlib import Path
from typing import Any, Optional

from app.agent.tools.base import BaseTool, ToolSchema
from app.agent.types import RetrievedDocument


class IndicatorTool(BaseTool):
    """
    Get documentation for a specific pandas-ta indicator.

    Performs direct file lookup by indicator name, providing
    faster access than semantic search when the exact indicator
    is known.
    """

    def __init__(self, corpus_dir: Path):
        """
        Initialize with corpus directory path.

        Args:
            corpus_dir: Path to app/corpus directory.
        """
        self.corpus_dir = Path(corpus_dir)
        self.indicators_dir = self.corpus_dir / 'indicators'

    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name='get_indicator_info',
            description='Get detailed documentation for a specific pandas-ta indicator by name',
            parameters={
                'indicator_name': {
                    'type': 'string',
                    'description': 'Name of the indicator (e.g., "rsi", "ema", "bbands")'
                }
            },
            required=['indicator_name']
        )

    def _execute(self, indicator_name: str) -> Optional[RetrievedDocument]:
        """
        Look up indicator documentation by name.

        Args:
            indicator_name: Indicator name (case-insensitive).

        Returns:
            RetrievedDocument if found, None if not found.

        Raises:
            FileNotFoundError: If indicator documentation not found.
        """
        # Normalize name to lowercase
        name_lower = indicator_name.lower().strip()

        # Try exact match first
        doc_path = self.indicators_dir / f"{name_lower}.md"

        if not doc_path.exists():
            # Try common variations
            variations = [
                name_lower,
                name_lower.replace('_', ''),
                name_lower.replace('-', ''),
            ]

            found = False
            for variation in variations:
                doc_path = self.indicators_dir / f"{variation}.md"
                if doc_path.exists():
                    found = True
                    break

            if not found:
                raise FileNotFoundError(
                    f"No documentation found for indicator: {indicator_name}. "
                    f"Searched in {self.indicators_dir}"
                )

        # Read and parse document
        content = doc_path.read_text(encoding='utf-8')

        # Extract title from first line
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else indicator_name.upper()

        return RetrievedDocument(
            doc_id=f"indicators_{name_lower}",
            content=content,
            title=title,
            category='indicators',
            relevance_score=1.0,  # Exact match
            concepts=None
        )

    def list_available(self) -> list:
        """Return list of all available indicator names."""
        if not self.indicators_dir.exists():
            return []

        return [
            f.stem for f in self.indicators_dir.glob('*.md')
        ]
