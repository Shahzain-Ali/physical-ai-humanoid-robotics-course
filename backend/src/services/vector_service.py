"""
Vector service for the RAG Chatbot backend.

This module provides functionality to interact with the Qdrant vector database
for semantic search and content retrieval operations.
"""
import os
from typing import List, Dict, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class VectorService:
    """
    Service class for handling vector database operations with Qdrant.
    """

    def __init__(self, collection_name: str = "book_content"):
        """
        Initialize the vector service.

        Args:
            collection_name: Name of the Qdrant collection to use
        """
        self.collection_name = collection_name

        # Initialize Qdrant async client
        qdrant_url = os.getenv("QDRANT_URL", "").strip()
        qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment variables")

        self.client = AsyncQdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=30
        )

    async def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """
        Search for similar content in the vector database.

        Args:
            query_embedding: Embedding vector to search for similar items
            limit: Maximum number of results to return

        Returns:
            List of similar content with metadata
        """
        try:
            # Perform semantic search in Qdrant
            search_results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )

            # Format results
            results = []
            for hit in search_results:
                result = {
                    "id": hit.id,
                    "text": hit.payload.get("text", ""),
                    "page": hit.payload.get("page", ""),
                    "section": hit.payload.get("section", ""),
                    "url": hit.payload.get("url", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "token_count": hit.payload.get("token_count", 0),
                    "relevance_score": hit.score
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error searching for similar content: {e}")
            raise

    async def add_documents(self, documents: List[Dict]) -> bool:
        """
        Add documents to the vector database.

        Args:
            documents: List of document dictionaries with text, embedding, and metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            points = []
            for doc in documents:
                point = PointStruct(
                    id=doc["id"],
                    vector=doc["embedding"],
                    payload={
                        "text": doc["text"],
                        "page": doc["page"],
                        "section": doc["section"],
                        "url": doc["url"],
                        "chunk_index": doc["chunk_index"],
                        "token_count": doc["token_count"]
                    }
                )
                points.append(point)

            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error adding documents to vector database: {e}")
            return False

    async def get_collection_info(self) -> Dict:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection information
        """
        try:
            collection_info = await self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_info.points_count,
                "config": {
                    "hnsw_config": collection_info.config.hnsw_config.dict() if collection_info.config.hnsw_config else None,
                    "optimizer_config": collection_info.config.optimizer_config.dict() if collection_info.config.optimizer_config else None
                }
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            raise

    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector database.

        Args:
            doc_id: ID of the document to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[doc_id])
            )
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

    async def update_document(self, doc_id: str, text: str, embedding: List[float], metadata: Dict) -> bool:
        """
        Update a document in the vector database.

        Args:
            doc_id: ID of the document to update
            text: Updated text content
            embedding: Updated embedding vector
            metadata: Updated metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            point = PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "text": text,
                    "page": metadata.get("page", ""),
                    "section": metadata.get("section", ""),
                    "url": metadata.get("url", ""),
                    "chunk_index": metadata.get("chunk_index", 0),
                    "token_count": metadata.get("token_count", 0)
                }
            )

            await self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def search_by_metadata(self, metadata_filters: Dict, limit: int = 10) -> List[Dict]:
        """
        Search documents by metadata filters.

        Args:
            metadata_filters: Dictionary of metadata fields to filter by
            limit: Maximum number of results to return

        Returns:
            List of matching documents
        """
        try:
            # Build filter conditions
            must_conditions = []
            for key, value in metadata_filters.items():
                must_conditions.append(
                    models.FieldCondition(
                        key=f"payload.{key}",
                        match=models.MatchValue(value=value)
                    )
                )

            filter_obj = models.Filter(must=must_conditions)

            search_results = await self.client.search(
                collection_name=self.collection_name,
                query_filter=filter_obj,
                limit=limit,
                with_payload=True
            )

            results = []
            for hit in search_results:
                result = {
                    "id": hit.id,
                    "text": hit.payload.get("text", ""),
                    "page": hit.payload.get("page", ""),
                    "section": hit.payload.get("section", ""),
                    "url": hit.payload.get("url", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "token_count": hit.payload.get("token_count", 0),
                    "relevance_score": hit.score
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error searching by metadata: {e}")
            raise

    async def search_with_context(self, query_embedding: List[float], context_size: int = 3, limit: int = 5) -> List[Dict]:
        """
        Search for similar content and include surrounding context.

        Args:
            query_embedding: Embedding vector to search for similar items
            context_size: Number of surrounding chunks to include
            limit: Maximum number of results to return

        Returns:
            List of content with context
        """
        try:
            # First, get the similar chunks
            similar_chunks = await self.search_similar(query_embedding, limit=limit)

            # For each chunk, potentially retrieve context from neighboring chunks
            results_with_context = []
            for chunk in similar_chunks:
                # In a full implementation, we would retrieve neighboring chunks
                # For now, we'll just return the chunk with its existing info
                results_with_context.append(chunk)

            return results_with_context
        except Exception as e:
            print(f"Error searching with context: {e}")
            raise


# Global instance for use in other modules
vector_service = VectorService()