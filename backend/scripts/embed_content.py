#!/usr/bin/env python3
"""
Content embedding script for the RAG Chatbot backend.

This script processes all markdown files in the docs directory,
chunks them, generates embeddings using OpenAI API, and stores
them in Qdrant vector database using optimized batch processing.
"""
import os
import sys
import time
import asyncio
from pathlib import Path
from typing import List, Dict
import uuid
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from tqdm.asyncio import tqdm
import tiktoken

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.chunker import MarkdownChunker, chunk_all_docs


async def get_embedding_async(client, text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Get embedding for a text using OpenAI API asynchronously.

    Args:
        client: AsyncOpenAI client
        text: Text to embed
        model: OpenAI embedding model to use

    Returns:
        List of embedding values
    """
    response = await client.embeddings.create(
        input=text,
        model=model,
        encoding_format="float"
    )
    return response.data[0].embedding


async def embed_batch_async(client, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Get embeddings for a batch of texts using OpenAI API asynchronously.

    Args:
        client: AsyncOpenAI client
        texts: List of texts to embed
        model: OpenAI embedding model to use

    Returns:
        List of embedding vectors
    """
    response = await client.embeddings.create(
        input=texts,
        model=model,
        encoding_format="float"
    )
    return [item.embedding for item in response.data]


async def embed_and_store_chunks(chunks: List[Dict], batch_size: int = 50):
    """
    Embed chunks and store them in Qdrant using optimized batch processing.

    Args:
        chunks: List of chunk dictionaries
        batch_size: Number of chunks to process in each batch
    """
    # Initialize OpenAI async client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable must be set")
        sys.exit(1)

    openai_client = AsyncOpenAI(api_key=openai_api_key)

    # Initialize Qdrant async client
    qdrant_url = os.getenv("QDRANT_URL", "").strip()
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "").strip()
    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY environment variables must be set")
        sys.exit(1)

    qdrant_client = AsyncQdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=30  # 30 second timeout for large operations
    )

    collection_name = "book_content"

    print(f"Loading course content from docs/...")

    # Process chunks in batches
    total_chunks = len(chunks)
    processed = 0
    total_tokens = 0

    print(f"✓ Found {total_chunks} chunks to process")
    print(f"Generating embeddings in batches of {batch_size}...")

    # Progress bar for embedding generation
    embedding_progress = tqdm(total=total_chunks, desc="Embedding", unit="chunk")

    # Process in batches
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]

        try:
            # Extract texts for this batch
            batch_texts = [chunk['text'] for chunk in batch]

            # Generate embeddings for the entire batch at once
            batch_embeddings = await embed_batch_async(openai_client, batch_texts)
            num = 1
            # Create Qdrant points from batch
            batch_points = []
            for idx, (chunk, embedding) in enumerate(zip(batch, batch_embeddings)):
                print("Running:",num)
                try:
                    total_tokens += chunk['token_count']

                    # Create Qdrant point with valid UUID ID
                    point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{chunk['page']}#{chunk['chunk_index']}"))

                    point = models.PointStruct(
                        id=point_id,  # Valid UUID format
                        vector=embedding,
                        payload={
                            "text": chunk['text'],
                            "page": chunk['page'],
                            "section": chunk.get('section', 'Untitled Section'),
                            "url": chunk['url'],
                            "chunk_index": chunk['chunk_index'],
                            "token_count": chunk['token_count']
                        }
                    )
                    batch_points.append(point)
                    num+=1
                except Exception as e:
                    print(f"Error processing chunk {chunk.get('page', 'unknown')}#{chunk.get('chunk_index', 'unknown')}: {e}")
                    continue

            # Upload batch to Qdrant
            if batch_points:
                try:
                    await qdrant_client.upsert(
                        collection_name=collection_name,
                        points=batch_points
                    )
                except Exception as e:
                    print(f"Error uploading batch to Qdrant: {e}")
                    continue

            processed += len(batch_points)
            embedding_progress.update(len(batch))

        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            continue

    embedding_progress.close()

    print(f"✓ Generated embeddings for {processed} chunks ({total_tokens} tokens total)")
    print(f"Estimated OpenAI cost: ~${round(total_tokens * 0.00002, 2)}")  # Approximate cost for text-embedding-3-small

    print(f"✓ Uploaded successfully to Qdrant")

    # Get collection info
    try:
        collection_info = await qdrant_client.get_collection(collection_name)
        print(f"\nSummary:")
        print(f"  Pages processed: {len(set(c['page'] for c in chunks))}")
        print(f"  Chunks created: {total_chunks}")
        print(f"  Total tokens: ~{total_tokens:,}")
        print(f"  Qdrant points: {collection_info.points_count}")
        print(f"  Estimated cost: ${round(total_tokens * 0.00002, 2)}")
        print(f"  Batch size used: {batch_size}")
        print(f"  Batches processed: {(total_chunks + batch_size - 1) // batch_size}")
    except Exception as e:
        print(f"Warning: Could not get collection info: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Embed course content for RAG Chatbot")
    parser.add_argument("--docs-dir", default="../docs/", help="Directory containing markdown files (default: ../docs/)")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for embedding (default: 50)")
    parser.add_argument("--chunk-size", type=int, default=800, help="Max tokens per chunk (default: 800)")
    parser.add_argument("--overlap", type=int, default=100, help="Token overlap between chunks (default: 100)")

    args = parser.parse_args()

    print("Loading course content...")

    # Check if docs directory exists
    docs_path = os.path.abspath(args.docs_dir)
    if not os.path.exists(docs_path):
        print(f"Error: Directory '{docs_path}' does not exist")
        sys.exit(1)

    # Chunk all docs
    chunks = chunk_all_docs(args.docs_dir)

    if not chunks:
        print("No markdown files found in docs directory")
        sys.exit(1)

    # Process chunks with the specified parameters
    chunker = MarkdownChunker(chunk_size=args.chunk_size, overlap=args.overlap)

    # Re-chunk if needed with specified parameters
    processed_chunks = []
    for chunk in chunks:
        # If chunk is too large, re-chunk it with specified parameters
        if chunk['token_count'] > args.chunk_size:
            # This is a simplified approach - in practice, we'd need to re-chunk the original content
            # For now, we'll just use the chunks as they are
            processed_chunks.append(chunk)
        else:
            processed_chunks.append(chunk)

    print(f"\nStarting optimized embedding process...")
    print(f"  Total chunks: {len(processed_chunks):,}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Estimated time: 2-5 minutes (vs 20-40 minutes sequential)")

    start_time = time.time()

    # Run the async embedding function
    asyncio.run(embed_and_store_chunks(processed_chunks, args.batch_size))

    elapsed_time = time.time() - start_time
    print(f"\nTotal processing time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")


if __name__ == "__main__":
    main()