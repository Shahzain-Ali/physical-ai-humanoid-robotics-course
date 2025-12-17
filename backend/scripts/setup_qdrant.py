#!/usr/bin/env python3
"""
Qdrant setup script for the RAG Chatbot backend.

This script creates the necessary Qdrant collection for storing
course content embeddings with appropriate configuration.
"""
import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

# Load environment variables from .env file
load_dotenv()


def setup_qdrant_collection(
    collection_name: str = "book_content",
    vector_size: int = 1536,  # OpenAI text-embedding-3-small dimension
    distance: str = "Cosine",
    recreate: bool = False
):
    """
    Setup Qdrant collection for storing course content embeddings.

    Args:
        collection_name: Name of the collection to create
        vector_size: Size of the embedding vectors (default: 1536 for OpenAI)
        distance: Distance metric for similarity search (default: Cosine)
        recreate: Whether to recreate the collection if it exists
    """
    # Get Qdrant configuration from environment
    qdrant_url = os.getenv("QDRANT_URL", "").strip()
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()

    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY environment variables must be set")
        sys.exit(1)

    print(f"Connecting to Qdrant at {qdrant_url}...")

    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=10  # 10 second timeout
        )

        # Check if collection already exists
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        if collection_name in collection_names:
            if recreate:
                print(f"Collection '{collection_name}' already exists. Recreating...")
                client.delete_collection(collection_name)
                print(f"✓ Collection '{collection_name}' deleted")
            else:
                print(f"Collection '{collection_name}' already exists.")
                print("Use --recreate flag to recreate the collection.")
                return

        # Create collection with HNSW indexing for fast similarity search
        print(f"Creating collection '{collection_name}'...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance[distance.upper()]
            ),
            # Configure HNSW indexing for fast approximate search
            hnsw_config=models.HnswConfigDiff(
                m=16,              # Max number of edges per node
                ef_construct=100   # Construction time/quality trade-off
            ),
            # Configure optimizers for efficient storage
            optimizers_config=models.OptimizersConfigDiff(
                memmap_threshold=20000,    # Use memory mapping for efficiency
                indexing_threshold=20000,  # Index vectors in memory
                max_segment_size=100000,
                flush_interval_sec=5
            ),
            # Enable payload indexing for efficient filtering
            wal_config=models.WalConfigDiff(
                wal_capacity_mb=32,
                wal_segments_ahead=0
            )
        )

        print(f"✓ Collection '{collection_name}' created with config:")
        print(f"  - Vector size: {vector_size}")
        print(f"  - Distance metric: {distance}")
        print(f"  - HNSW parameters: m=16, ef_construct=100, ef=200")
        print("✓ Setup complete!")

    except UnexpectedResponse as e:
        print(f"Error: Failed to create collection - {e}")
        print("This might be due to invalid API key or URL.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to connect to Qdrant - {e}")
        sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Setup Qdrant collection for RAG Chatbot")
    parser.add_argument("--collection", default="book_content", help="Collection name (default: book_content)")
    parser.add_argument("--vector-size", type=int, default=1536, help="Vector size (default: 1536 for OpenAI embeddings)")
    parser.add_argument("--distance", default="Cosine", choices=["Cosine", "Euclid", "Dot"], help="Distance metric (default: Cosine)")
    parser.add_argument("--recreate", action="store_true", help="Recreate collection if it exists")

    args = parser.parse_args()

    setup_qdrant_collection(
        collection_name=args.collection,
        vector_size=args.vector_size,
        distance=args.distance,
        recreate=args.recreate
    )


if __name__ == "__main__":
    main()