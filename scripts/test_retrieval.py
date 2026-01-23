"""
Test retrieval across indicator and price_action corpora.
Verifies that both document types are searchable.
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

CHROMA_DIR = Path(__file__).parent.parent / 'data' / 'chroma'
COLLECTION_NAME = 'strategy_docs'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'


def test_retrieval():
    """Test retrieval with queries spanning both corpora."""
    print("=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    print(f"\nCollection has {collection.count()} documents\n")

    # Test queries
    test_queries = [
        # Indicator queries
        ("RSI overbought oversold", "indicators"),
        ("moving average crossover", "indicators"),
        ("Bollinger Bands volatility", "indicators"),

        # Price action queries
        ("market structure higher highs", "price_action"),
        ("reversal entry setup", "price_action"),
        ("protected swing stop loss", "price_action"),
        ("timeframe alignment bias", "price_action"),

        # Mixed queries
        ("mean reversion strategy entry rules", "mixed"),
        ("trend following continuation signals", "mixed"),
    ]

    for query, expected_source in test_queries:
        print(f"\nQuery: \"{query}\"")
        print(f"Expected source: {expected_source}")
        print("-" * 40)

        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=['metadatas', 'documents']
        )

        for i, (meta, doc) in enumerate(zip(results['metadatas'][0], results['documents'][0])):
            category = meta.get('category', 'unknown')
            title = meta.get('title', 'untitled')
            snippet = doc[:100].replace('\n', ' ') + '...'
            print(f"  {i+1}. [{category}] {title}")
            print(f"     {snippet}")

    # Category breakdown
    print("\n" + "=" * 60)
    print("CATEGORY BREAKDOWN")
    print("=" * 60)

    all_docs = collection.get(include=['metadatas'])
    categories = {}
    for meta in all_docs['metadatas']:
        cat = meta.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} documents")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    test_retrieval()
