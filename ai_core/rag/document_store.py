import os
from uuid import UUID

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentStore:
    def __init__(self, 
        embedding: OllamaEmbeddings, 
        splitter_chunk_size: int = 500, 
        splitter_chunk_overlap: int = 100
    ):
        self.vector_store = Chroma(collection_name="rag_docs", embedding_function=embedding, persist_directory=os.getenv("CHROMA_DB_LOCATION") or './chroma_db')
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=splitter_chunk_size, chunk_overlap=splitter_chunk_overlap)

    def add_document(
        self,
        campaign_id: int,
        document_id: UUID,
        filename: str,
        text: str
    ) -> None:
        chunks = self.splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "campaign_id": str(campaign_id),
                    "document_id": str(document_id),
                    "filename": filename,
                    "chunk_index": index
                }
            )
            for index, chunk in enumerate(chunks)
        ]

        chunk_ids = [f"{campaign_id}:{document_id}:{index}" for index in range(len(chunks))]
        self.vector_store.add_documents(documents, ids=chunk_ids)

    def get_document(self, campaign_id: int, document_id: UUID):
        return self.vector_store.get(
        where={
            "$and": [
                {"campaign_id": str(campaign_id)},
                {"document_id": str(document_id)},
            ]
        },
        include=["documents", "metadatas"]
        )

    def search(self, campaign_id: int, query: str, limit: int = 5):
        return self.vector_store.similarity_search(
            query=query,
            k=limit,
            filter={"campaign_id": str(campaign_id)}
        )

    def delete_document(self, campaign_id: int, document_id: UUID) -> None:
        self.vector_store.delete(where={"$and": [{"campaign_id": str(campaign_id)}, {"document_id": str(document_id)}]})

    def update_document(self, campaign_id: int, document_id: UUID, new_text: str) -> None:
        self.delete_document(campaign_id, document_id)
        self.add_document(campaign_id, document_id, f"{document_id}.txt", new_text)

    @staticmethod
    def get_file_extension(filename: str) -> str:
        return filename.split('.')[-1].lower()
