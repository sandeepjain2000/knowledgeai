"""
chunker.py — Split document text into overlapping word-based chunks.
             Each chunk is tagged with its source page number when available.
"""
from typing import List, Dict, Optional
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, doc_id: str, file_name: str,
               chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP,
               page_word_offsets: Optional[List] = None) -> List[Dict]:
    """
    Split text into chunks of ~chunk_size words with overlap.

    page_word_offsets: list of (page_num, start_word_index) tuples, sorted ascending.
      Provided by the PDF parser. When present, each chunk is tagged with its page_num.
      When absent (DOCX/TXT), page_num defaults to 1.

    Returns list of dicts: {chunk_id, doc_id, file_name, text, word_count,
                             chunk_index, page_num}
    """
    words = text.split()
    chunks = []
    start = 0
    idx = 0

    # Build sorted offset list for binary-search-style lookup
    offsets = sorted(page_word_offsets, key=lambda x: x[1]) if page_word_offsets else []

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words)

        # Find the page this chunk starts on
        page_num = _word_to_page(start, offsets)

        chunk_id = f"{doc_id}_chunk_{idx:04d}"
        chunks.append({
            "chunk_id":    chunk_id,
            "doc_id":      doc_id,
            "file_name":   file_name,
            "text":        chunk_text_str,
            "word_count":  len(chunk_words),
            "chunk_index": idx,
            "page_num":    page_num,
        })

        # Advance, keeping overlap
        step = max(1, chunk_size - overlap)
        start += step
        idx += 1

    return chunks


def _word_to_page(word_idx: int, offsets: List) -> int:
    """Return the 1-based page number for word at word_idx."""
    if not offsets:
        return 1
    page_num = offsets[0][0]   # default to first page
    for p_num, p_start in offsets:
        if word_idx >= p_start:
            page_num = p_num
        else:
            break
    return page_num
