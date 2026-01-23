"""
RESEARCH state handler.

Gathers relevant information from the knowledge base using
targeted retrieval based on the decomposed request.
"""

from typing import List, Tuple, Set

from app.agent.states.base import StateHandler
from app.agent.types import (
    AgentContext,
    AgentState,
    ResearchFindings,
    RetrievedDocument,
    ToolCall,
)
from app.agent.tools import RetrieveTool, IndicatorTool


class ResearchHandler(StateHandler):
    """
    Gather relevant information via targeted retrieval.

    Uses the research queries from decomposition to search
    both indicator documentation and price action content.
    Also performs direct lookups for specifically mentioned indicators.
    """

    def __init__(
        self,
        retrieve_tool: RetrieveTool,
        indicator_tool: IndicatorTool,
        max_queries: int = 8
    ):
        """
        Initialize with retrieval tools.

        Args:
            retrieve_tool: Tool for semantic search.
            indicator_tool: Tool for direct indicator lookup.
            max_queries: Maximum number of retrieval queries to execute.
        """
        self.retrieve_tool = retrieve_tool
        self.indicator_tool = indicator_tool
        self.max_queries = max_queries
        self._tool_calls: List[ToolCall] = []

    @property
    def state(self) -> AgentState:
        return AgentState.RESEARCH

    def validate_entry(self, context: AgentContext) -> bool:
        """
        Validate context for RESEARCH state.

        Requires decomposed_request with research queries.
        """
        if not context.decomposed_request:
            return False
        if not context.decomposed_request.research_queries:
            return False
        return True

    def execute(self, context: AgentContext) -> Tuple[AgentContext, AgentState]:
        """
        Execute research phase.

        Args:
            context: Agent context with decomposed_request.

        Returns:
            Updated context with research_findings, next state.
        """
        self._tool_calls = []

        try:
            findings = self._gather_research(context)
            context.research_findings = findings

            # Check if we got any useful documents
            if findings.total_documents == 0:
                context.warnings.append(
                    "No relevant documents found. Proceeding with LLM knowledge only."
                )

            return context, AgentState.SYNTHESIZE

        except Exception as e:
            context.errors.append(f"Research failed: {str(e)}")
            return context, AgentState.FAILED

    def _gather_research(self, context: AgentContext) -> ResearchFindings:
        """
        Execute research queries and gather documents.

        Args:
            context: Agent context with decomposed request.

        Returns:
            Aggregated research findings.
        """
        decomposed = context.decomposed_request
        all_documents: List[RetrievedDocument] = []
        seen_ids: Set[str] = set()
        queries_executed: List[str] = []

        # 1. Direct lookup for specifically mentioned indicators
        if decomposed.indicators:
            for indicator_name in decomposed.indicators:
                result = self.indicator_tool.execute(indicator_name=indicator_name)
                self._tool_calls.append(result)

                if result.success and result.result:
                    doc = result.result
                    if doc.doc_id not in seen_ids:
                        all_documents.append(doc)
                        seen_ids.add(doc.doc_id)

        # 2. Execute research queries with category-aware retrieval
        query_count = 0
        for query in decomposed.research_queries:
            if query_count >= self.max_queries:
                break

            # Determine best category based on query content
            category = self._determine_category(query)

            result = self.retrieve_tool.execute(
                query=query,
                category=category,
                top_k=3
            )
            self._tool_calls.append(result)
            queries_executed.append(query)
            query_count += 1

            if result.success and result.result:
                for doc in result.result:
                    if doc.doc_id not in seen_ids:
                        all_documents.append(doc)
                        seen_ids.add(doc.doc_id)

        # 3. If we have few results, broaden the search
        if len(all_documents) < 3 and query_count < self.max_queries:
            # Try a general search with the original query
            result = self.retrieve_tool.execute(
                query=context.original_query,
                category='all',
                top_k=5
            )
            self._tool_calls.append(result)
            queries_executed.append(f"[fallback] {context.original_query}")

            if result.success and result.result:
                for doc in result.result:
                    if doc.doc_id not in seen_ids:
                        all_documents.append(doc)
                        seen_ids.add(doc.doc_id)

        # Categorize documents
        indicator_docs = [d for d in all_documents if d.category == 'indicators']
        price_action_docs = [d for d in all_documents if d.category == 'price_action']

        # Identify gaps
        gaps = self._identify_gaps(decomposed, all_documents)

        return ResearchFindings(
            queries_executed=queries_executed,
            documents=all_documents,
            indicator_docs=indicator_docs,
            price_action_docs=price_action_docs,
            gaps_identified=gaps
        )

    def _determine_category(self, query: str) -> str:
        """
        Determine best category for a query based on content.

        Args:
            query: Search query string.

        Returns:
            Category string: 'indicators', 'price_action', or 'all'.
        """
        query_lower = query.lower()

        # Indicator-related keywords
        indicator_keywords = [
            'indicator', 'rsi', 'macd', 'ema', 'sma', 'bollinger',
            'moving average', 'oscillator', 'momentum indicator',
            'volume indicator', 'atr', 'adx', 'stochastic'
        ]

        # Price action keywords (includes TTrades terminology)
        price_action_keywords = [
            'market structure', 'reversal', 'reversal signature', 'consolidation',
            'expansion', 'retracement', 'entry', 'exit', 'stop loss', 'protected swing',
            'timeframe', 'higher high', 'lower low', 'support', 'resistance',
            'breakout', 'pullback', 'trend', 'cisd', 'phases', 'blending'
        ]

        indicator_score = sum(1 for kw in indicator_keywords if kw in query_lower)
        price_action_score = sum(1 for kw in price_action_keywords if kw in query_lower)

        if indicator_score > price_action_score:
            return 'indicators'
        elif price_action_score > indicator_score:
            return 'price_action'
        else:
            return 'all'

    def _identify_gaps(
        self,
        decomposed,
        documents: List[RetrievedDocument]
    ) -> List[str]:
        """
        Identify information gaps in research.

        Args:
            decomposed: Decomposed request.
            documents: Retrieved documents.

        Returns:
            List of identified gaps.
        """
        gaps = []

        # Check if we found docs for requested indicators
        if decomposed.indicators:
            doc_titles = {d.title.lower() for d in documents}
            for indicator in decomposed.indicators:
                if indicator.lower() not in doc_titles:
                    gaps.append(f"No documentation found for indicator: {indicator}")

        # Check if we have entry/exit guidance
        has_entry_docs = any(
            'entry' in d.title.lower() or 'entry' in str(d.concepts or []).lower()
            for d in documents
        )
        if decomposed.entry_requirements and not has_entry_docs:
            gaps.append("Limited entry logic documentation found")

        return gaps

    def get_tool_calls(self) -> List[ToolCall]:
        """Return tool calls made during execution."""
        return self._tool_calls
