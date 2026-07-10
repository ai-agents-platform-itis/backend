from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.knowledge_doc import KnowledgeDocService
from app.schemas.knowledge_doc import KnowledgeDocResponse

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


@router.get("/{doc_id}", response_model=KnowledgeDocResponse)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """Получить полный текст документа (для ChromaDB)."""
    service = KnowledgeDocService(db)
    try:
        return await service.get_document_content(doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))