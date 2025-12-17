"""
Content chunking utility for the RAG Chatbot backend.

This module provides functionality to split markdown content into
semantically meaningful chunks for vector storage and retrieval.
"""
import re
from typing import List, Dict, Tuple
import tiktoken


class MarkdownChunker:
    """
    Utility class for chunking markdown content intelligently.
    """

    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        """
        Initialize the chunker with specific parameters.

        Args:
            chunk_size: Maximum number of tokens per chunk
            overlap: Number of tokens to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.encoding_for_model("gpt-4")

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text: Input text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return len(self.encoding.encode(text))

    def split_by_headers(self, content: str) -> List[str]:
        """
        Split content by markdown headers while preserving header context.

        Args:
            content: Markdown content to split

        Returns:
            List of content sections split by headers
        """
        # Split by H2 and H3 headers, keeping the headers with the content
        header_pattern = r'(\n##\s+.*?\n|\n###\s+.*?\n)'
        parts = re.split(header_pattern, content)

        # Reconstruct sections with headers
        sections = []
        current_section = ""

        for part in parts:
            if re.match(r'\n##\s+|\n###\s+', part):
                # If we have accumulated content, save it before starting new section
                if current_section.strip():
                    sections.append(current_section.strip())
                # Start new section with header
                current_section = part
            else:
                current_section += part

        # Add the last section if it exists
        if current_section.strip():
            sections.append(current_section.strip())

        return sections

    def chunk_text(self, text: str, source_page: str, url: str) -> List[Dict]:
        """
        Chunk a text string into smaller pieces based on token count.

        Args:
            text: Text to chunk
            source_page: Name of the source page
            url: URL to the source page

        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        tokens = self.encoding.encode(text)

        # If the text is small enough, return as single chunk
        if len(tokens) <= self.chunk_size:
            return [{
                'text': text,
                'page': source_page,
                'url': url,
                'token_count': len(tokens),
                'embedding': None  # Will be filled in later
            }]

        # Otherwise, split into overlapping chunks
        start_idx = 0
        chunk_idx = 0

        while start_idx < len(tokens):
            # Get chunk of specified size
            end_idx = start_idx + self.chunk_size

            # Ensure we don't exceed the text length
            if end_idx > len(tokens):
                end_idx = len(tokens)

            # Decode tokens back to text
            chunk_text = self.encoding.decode(tokens[start_idx:end_idx])

            # Create chunk with metadata
            chunk = {
                'text': chunk_text,
                'page': source_page,
                'url': url,
                'token_count': end_idx - start_idx,
                'chunk_index': chunk_idx,
                'embedding': None  # Will be filled in later
            }

            chunks.append(chunk)

            # Move to next chunk with overlap
            if end_idx >= len(tokens):
                break  # We've reached the end

            # Calculate next start position with overlap
            start_idx = end_idx - self.overlap
            chunk_idx += 1

            # Ensure we don't have negative overlap
            if start_idx < 0:
                start_idx = 0

        return chunks

    def chunk_markdown_file(self, file_path: str, source_page: str) -> List[Dict]:
        """
        Chunk a markdown file into semantically meaningful pieces.

        Args:
            file_path: Path to the markdown file
            source_page: Name of the source page (for metadata)

        Returns:
            List of chunk dictionaries with metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract the URL from the file path (convert docs/03-ros2.md to docs/03-ros2)
        # Note: No leading slash to avoid double slashes when combined with base URL
        url_path = file_path.replace('../docs/', '').replace('.md', '')

        # First, split by headers to get semantically coherent sections
        sections = self.split_by_headers(content)

        all_chunks = []

        for i, section in enumerate(sections):
            # Count tokens in the section
            section_tokens = self.count_tokens(section)

            if section_tokens <= self.chunk_size:
                # Section fits in a single chunk
                all_chunks.append({
                    'text': section.strip(),
                    'page': source_page,
                    'url': url_path,
                    'section': self._extract_section_title(section),
                    'token_count': section_tokens,
                    'chunk_index': len(all_chunks),
                    'embedding': None
                })
            else:
                # Section is too large, split further by token count
                sub_chunks = self.chunk_text(section, source_page, url_path)
                for chunk in sub_chunks:
                    chunk['chunk_index'] = len(all_chunks)
                    chunk['section'] = self._extract_section_title(section)
                    all_chunks.append(chunk)

        return all_chunks

    def _extract_section_title(self, content: str) -> str:
        """
        Extract the section title from content (first H2 or H3 header).

        Args:
            content: Content to extract title from

        Returns:
            Section title or 'Untitled' if no header found
        """
        # Look for H2 or H3 headers at the beginning of the content
        header_match = re.search(r'^(##|###)\s+(.+?)(\n|$)', content.strip())
        if header_match:
            return header_match.group(2).strip()
        return "Untitled Section"


def chunk_all_docs(docs_dir: str = "docs/") -> List[Dict]:
    """
    Chunk all markdown files in the docs directory.

    Args:
        docs_dir: Directory containing markdown files

    Returns:
        List of all chunks from all files
    """
    import os
    from pathlib import Path

    chunker = MarkdownChunker()
    all_chunks = []

    # Find all markdown files in the docs directory
    for file_path in Path(docs_dir).glob("**/*.md"):
        source_page = str(file_path).split("/")[-1]  # Get just the filename
        try:
            file_chunks = chunker.chunk_markdown_file(str(file_path), source_page)
            all_chunks.extend(file_chunks)
            print(f"Chunked {file_path} into {len(file_chunks)} chunks")
        except Exception as e:
            print(f"Error chunking {file_path}: {e}")

    return all_chunks