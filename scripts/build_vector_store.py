"""
Build vector store from corpus documents.
to be run after build_corpus.py to create searchable embeddings.
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

CORPUS_DIR = Path(__file__).parent.parent / 'app' / 'corpus'
CHROMA_DIR = Path(__file__).parent.parent / 'data' / 'chroma'
COLLECTION_NAME = 'strategy_docs'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'


def load_documents():
    """Load all markdown files from corpus."""
    documents = []

    for category_dir in CORPUS_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        category = category_dir.name

        for file_path in category_dir.glob('*.md'):
            content = file_path.read_text(encoding='utf-8')

            # Extract title from first line
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip() if lines else file_path.stem

            documents.append({
                'id': f"{category}_{file_path.stem}",
                'content': content,
                'metadata': {
                    'source': str(file_path),
                    'category': category,
                    'title': title
                }
            })

    return documents


def build_vector_store():
    """Build and persist the vector store."""
    print(f"Loading documents from {CORPUS_DIR}")
    documents = load_documents()
    print(f"Found {len(documents)} documents")

    if not documents:
        print("No documents found. Run build_corpus.py first.")
        return

    # Create embedding function
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    # Initialize ChromaDB
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    # Create new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"description": "Trading strategy documentation"}
    )

    # Add documents
    print("Adding documents to collection...")
    collection.add(
        ids=[doc['id'] for doc in documents],
        documents=[doc['content'] for doc in documents],
        metadatas=[doc['metadata'] for doc in documents]
    )

    print(f"\nDone! Vector store built at {CHROMA_DIR}")
    print(f"Collection '{COLLECTION_NAME}' contains {len(documents)} documents")


if __name__ == '__main__':
    build_vector_store()