"""Service for retrieving relevant documents from vector store."""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path


class RAGService:
  def __init__(self, chroma_dir, embedding_model='all-MiniLM-L6-v2'):
      self.chroma_dir = Path(chroma_dir)
      self.embedding_model = embedding_model
      self._collection = None

  def _get_collection(self):
      """Lazy load the collection."""
      if self._collection is None:
          embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
              model_name=self.embedding_model
          )

          client = chromadb.PersistentClient(path=str(self.chroma_dir))
          self._collection = client.get_collection(
              name='strategy_docs',
              embedding_function=embedding_fn
          )

      return self._collection

  def retrieve(self, query, top_k=5):
      """
      Find most relevant documents for a query.

      Args:
          query: User's strategy description
          top_k: Number of documents to retrieve

      Returns:
          List of relevant document contents
      """
      collection = self._get_collection()

      results = collection.query(
          query_texts=[query],
          n_results=top_k,
          include=['documents', 'metadatas']
      )

      documents = []
      for i in range(len(results['ids'][0])):
          documents.append({
              'content': results['documents'][0][i],
              'metadata': results['metadatas'][0][i]
          })

      return documents

  def format_context(self, documents):
      """Format retrieved documents for injection into prompt."""
      if not documents:
          return ""

      context_parts = ["## Relevant Indicator Documentation\n"]

      for doc in documents:
          title = doc['metadata'].get('title', 'Unknown')
          context_parts.append(f"### {title}\n")
          context_parts.append(doc['content'])
          context_parts.append("\n---\n")

      return '\n'.join(context_parts)