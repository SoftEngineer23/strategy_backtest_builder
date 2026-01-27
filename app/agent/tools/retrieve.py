"""
Retrieve tool for searching the knowledge base.

Wraps the RAG service to provide document retrieval with
category filtering and structured output.
"""

from typing import Any, List, Optional

from app.agent.tools.base import BaseTool, ToolSchema
from app.agent.types import RetrievedDocument
from app.services.rag_service import RAGService


class RetrieveTool(BaseTool):
    """
    Search the knowledge base for relevant documents.

    Supports filtering by category (indicators, price_action)
    and returns structured RetrievedDocument objects.
    """

    VALID_CATEGORIES = ['indicators', 'price_action', 'all']

    def __init__(self, rag_service: RAGService):
        """
        Initialize with RAG service instance.

        Args:
            rag_service: Configured RAGService for document retrieval.
        """
        self.rag_service = rag_service

    @property
    def schema(self) -> ToolSchema:
        return ToolSchema(
            name='retrieve',
            description='Search the knowledge base for relevant documents about indicators or price action concepts',
            parameters={
                'query': {
                    'type': 'string',
                    'description': 'Natural language search query'
                },
                'category': {
                    'type': 'string',
                    'enum': self.VALID_CATEGORIES,
                    'description': 'Filter by content category',
                    'default': 'all'
                },
                'top_k': {
                    'type': 'integer',
                    'description': 'Number of results to return',
                    'default': 5,
                    'minimum': 1,
                    'maximum': 10
                }
            },
            required=['query']
        )

    def _execute(
        self,
        query: str,
        category: str = 'all',
        top_k: int = 5
    ) -> List[RetrievedDocument]:
        """
        Execute retrieval query.

        Args:
            query: Search query string.
            category: Category filter (indicators, price_action, all).
            top_k: Maximum documents to return.

        Returns:
            List of RetrievedDocument objects.

        Raises:
            ValueError: If category is invalid.
        """
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Must be one of {self.VALID_CATEGORIES}")

        # Retrieve from RAG service
        # Request more than needed if filtering, to ensure enough results
        fetch_count = top_k if category == 'all' else top_k * 2
        raw_docs = self.rag_service.retrieve(query, top_k=fetch_count)

        # Convert to RetrievedDocument and apply category filter
        documents = []
        for i, doc in enumerate(raw_docs):
            metadata = doc.get('metadata', {})
            doc_category = metadata.get('category', 'unknown')

            # Apply category filter
            if category != 'all' and doc_category != category:
                continue

            # Extract concepts if available
            concepts_str = metadata.get('concepts', '')
            concepts = [c.strip() for c in concepts_str.split(',')] if concepts_str else None

            # Use actual doc_id from ChromaDB, fall back to generated ID
            doc_id = doc.get('id', f"{doc_category}_{i}")

            # Calculate relevance score from distance (lower distance = higher relevance)
            distance = doc.get('distance')
            if distance is not None:
                relevance_score = max(0.0, 1.0 - distance)
            else:
                relevance_score = 1.0 - (i * 0.1)

            retrieved_doc = RetrievedDocument(
                doc_id=doc_id,
                content=doc.get('content', ''),
                title=metadata.get('title', 'Unknown'),
                category=doc_category,
                relevance_score=relevance_score,
                concepts=concepts
            )
            documents.append(retrieved_doc)

            if len(documents) >= top_k:
                break

        return documents
