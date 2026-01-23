"""
Demo script showing the agent tools in action.

Run with: python scripts/demo_tools.py

This demonstrates:
1. Tool registration
2. Retrieve tool (semantic search with category filtering)
3. Indicator tool (direct lookup)
4. How ToolCall records capture results and timing
"""

from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.agent.tools import RetrieveTool, IndicatorTool
from app.agent.tool_registry import ToolRegistry
from app.services.rag_service import RAGService


def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_tool_call(result):
    """Pretty print a ToolCall result."""
    print(f"  Tool: {result.tool_name}")
    print(f"  Args: {result.arguments}")
    print(f"  Success: {result.success}")
    print(f"  Duration: {result.duration_ms:.1f}ms")
    if result.error:
        print(f"  Error: {result.error}")
    return result.result


def main():
    print_header("AGENT TOOLS DEMO")

    # Initialize services
    chroma_dir = project_root / 'data' / 'chroma'
    corpus_dir = project_root / 'app' / 'corpus'

    rag_service = RAGService(chroma_dir)

    # Create tools
    retrieve_tool = RetrieveTool(rag_service)
    indicator_tool = IndicatorTool(corpus_dir)

    # Create registry and register tools
    registry = ToolRegistry()
    registry.register(retrieve_tool)
    registry.register(indicator_tool)

    print(f"\nRegistered tools: {registry.list_tools()}")

    # -------------------------------------------------------------------------
    print_header("1. RETRIEVE TOOL - Search indicators")
    # -------------------------------------------------------------------------

    result = registry.execute('retrieve', query='RSI overbought oversold', category='indicators', top_k=3)
    docs = print_tool_call(result)

    print("\n  Results:")
    for doc in docs:
        print(f"    - [{doc.category}] {doc.title} (score: {doc.relevance_score:.2f})")

    # -------------------------------------------------------------------------
    print_header("2. RETRIEVE TOOL - Search price action")
    # -------------------------------------------------------------------------

    result = registry.execute('retrieve', query='how to identify market reversals', category='price_action', top_k=3)
    docs = print_tool_call(result)

    print("\n  Results:")
    for doc in docs:
        print(f"    - [{doc.category}] {doc.title}")
        if doc.concepts:
            print(f"      Concepts: {', '.join(doc.concepts[:4])}")

    # -------------------------------------------------------------------------
    print_header("3. RETRIEVE TOOL - Search all categories")
    # -------------------------------------------------------------------------

    result = registry.execute('retrieve', query='trend following momentum', category='all', top_k=4)
    docs = print_tool_call(result)

    print("\n  Results (mixed categories):")
    for doc in docs:
        print(f"    - [{doc.category}] {doc.title}")

    # -------------------------------------------------------------------------
    print_header("4. INDICATOR TOOL - Direct lookup")
    # -------------------------------------------------------------------------

    result = registry.execute('get_indicator_info', indicator_name='bbands')
    doc = print_tool_call(result)

    print(f"\n  Document: {doc.title}")
    print(f"  Category: {doc.category}")
    print(f"  Content preview: {doc.content[:200]}...")

    # -------------------------------------------------------------------------
    print_header("5. INDICATOR TOOL - Error handling")
    # -------------------------------------------------------------------------

    result = registry.execute('get_indicator_info', indicator_name='nonexistent_indicator')
    print_tool_call(result)
    print("\n  (Error was captured gracefully, not thrown)")

    # -------------------------------------------------------------------------
    print_header("6. TOOL SCHEMAS")
    # -------------------------------------------------------------------------

    print("\nEach tool has a schema describing its interface:\n")
    for schema in registry.get_schemas():
        print(f"  {schema.name}:")
        print(f"    Description: {schema.description[:60]}...")
        print(f"    Required params: {schema.required}")
        print()

    # -------------------------------------------------------------------------
    print_header("SUMMARY")
    # -------------------------------------------------------------------------

    print("""
What you just saw:

1. Tools wrap services (RAG, filesystem) with a uniform interface
2. Every execution returns a ToolCall with:
   - The result (or None on failure)
   - Timing information (duration_ms)
   - Success/failure status
   - Error message if failed

3. The ToolRegistry manages tools by name
4. Errors are captured, not thrown - graceful handling

Next phases will use these tools in state handlers:
- RESEARCH state uses RetrieveTool to gather context
- SYNTHESIZE state uses DraftTool to call Claude
- CRITIQUE state uses CritiqueTool to evaluate
""")


if __name__ == '__main__':
    main()
