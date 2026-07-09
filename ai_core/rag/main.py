import os
from langchain_ollama import OllamaEmbeddings

from rag.document_store import DocumentStore


embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL")
if not embedding_model:
    raise ValueError("OLLAMA_EMBEDDING_MODEL environment variable is not set.")

embedding = OllamaEmbeddings(model=embedding_model, base_url=os.getenv("OLLAMA_BASE_URL") or 'http://localhost:11434')
document_store = DocumentStore(embedding=embedding, splitter_chunk_size=500, splitter_chunk_overlap=100)

def get_document_store() -> DocumentStore:
    return document_store