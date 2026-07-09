from fastapi import APIRouter, FastAPI, HTTPException, Query, Depends, Response, status
from langchain_ollama import OllamaEmbeddings
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID, uuid4
from dotenv import load_dotenv
load_dotenv()
from rag import get_document_store, DocumentStore


app = FastAPI(title="RAG API", version="1.0.0")
router = APIRouter(prefix="/rag", tags=["RAG"])
app.include_router(router)

DocumentStoreDep = Annotated[DocumentStore, Depends(get_document_store)]


class DocumentCreate(BaseModel):
    filename: str
    text: str


class DocumentUpdate(BaseModel):
    new_text: str


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    text: str


class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    document_id: UUID
    filename: str
    chunk: str


@router.post(
    "/create",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    campaign_id: UUID,
    payload: DocumentCreate,
    store: DocumentStoreDep,
) -> DocumentResponse:
    document_id = uuid4()

    store.add_document(
        campaign_id=campaign_id,
        document_id=document_id,
        filename=payload.filename,
        text=payload.text,
    )

    return DocumentResponse(
        id=document_id,
        filename=payload.filename,
        text=payload.text,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    campaign_id: UUID,
    document_id: UUID,
    store: DocumentStoreDep,
) -> DocumentResponse:
    result = store.get_document(campaign_id, document_id)

    if not result["ids"]:
        raise HTTPException(404, "Document not found")

    chunks = sorted(
        zip(result["documents"], result["metadatas"]),
        key=lambda item: item[1]["chunk_index"],
    )

    return DocumentResponse(
        id=document_id,
        filename=chunks[0][1]["filename"],
        text="".join(chunk for chunk, _ in chunks),
    )


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    campaign_id: UUID,
    document_id: UUID,
    payload: DocumentUpdate,
    store: DocumentStoreDep,
) -> DocumentResponse:
    store.update_document(
        campaign_id=campaign_id,
        document_id=document_id,
        new_text=payload.new_text,
    )

    return DocumentResponse(
        id=document_id,
        filename=f"{document_id}.txt",
        text=payload.new_text,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    campaign_id: UUID,
    document_id: UUID,
    store: DocumentStoreDep,
) -> Response:
    store.delete_document(
        campaign_id=campaign_id,
        document_id=document_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/search", response_model=list[SearchResult])
def search_documents(
    campaign_id: UUID,
    payload: DocumentSearchRequest,
    store: DocumentStoreDep,
) -> list[SearchResult]:
    documents = store.search(
        campaign_id=campaign_id,
        query=payload.query,
        limit=payload.limit,
    )

    return [
        SearchResult(
            document_id=UUID(document.metadata["document_id"]),
            filename=document.metadata["filename"],
            chunk=document.page_content,
        )
        for document in documents
    ]