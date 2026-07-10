import os
from functools import lru_cache

from langchain_ollama import OllamaEmbeddings

from .document_store import DocumentStore


@lru_cache(maxsize=1)
def get_document_store() -> DocumentStore:
    embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL")
    if not embedding_model:
        raise ValueError("OLLAMA_EMBEDDING_MODEL environment variable is not set.")

    embeddings = OllamaEmbeddings(
        model=embedding_model,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

    return DocumentStore(
        embedding=embeddings,
        splitter_chunk_size=500,
        splitter_chunk_overlap=100,
    )
