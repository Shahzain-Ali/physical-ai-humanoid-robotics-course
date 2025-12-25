"""
Embedding service for the RAG Chatbot backend.

This module provides functionality to generate embeddings using OpenAI API
and manage embedding operations for the RAG system.
"""
import os
from typing import List, Optional
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv


# Load environment variables (override=True forces .env to override system env vars)
load_dotenv(override=True)

# Initialize OpenAI async client
# Strip any whitespace/carriage returns from API key
api_key = os.getenv("OPENAI_API_KEY", "").strip()
client = AsyncOpenAI(api_key=api_key)


class EmbeddingService:
    """
    Service class for handling embedding operations.
    """

    def __init__(self, model: str = "text-embedding-3-small", dimensions: int = 1536):
        """
        Initialize the embedding service.

        Args:
            model: OpenAI embedding model to use
            dimensions: Number of dimensions for embeddings (1536 for text-embedding-3-small)
        """
        self.model = model
        self.dimensions = dimensions

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            List of embedding values
        """
        try:
            response = await client.embeddings.create(
                input=text,
                model=self.model,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    async def batch_generate(self, texts: List[str], batch_size: int = 50) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = await client.embeddings.create(
                    input=batch,
                    model=self.model,
                    encoding_format="float"
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error generating embeddings for batch {i//batch_size}: {e}")
                raise

        return all_embeddings

    def get_embedding_length(self) -> int:
        """
        Get the expected length of embeddings for this service.

        Returns:
            Number of dimensions in the embedding
        """
        return self.dimensions

    async def embed_query(self, query: str) -> List[float]:
        """
        Embed a query for semantic search.

        Args:
            query: User query to embed

        Returns:
            Embedding vector for the query
        """
        return await self.generate_embedding(query)

    async def embed_document(self, document: str) -> List[float]:
        """
        Embed a document chunk for storage.

        Args:
            document: Document text to embed

        Returns:
            Embedding vector for the document
        """
        return await self.generate_embedding(document)


# Global instance for use in other modules
embedding_service = EmbeddingService()