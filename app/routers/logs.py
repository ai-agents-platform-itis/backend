from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.logs import LogsService
from app.schemas.dialog import DialogResponse, MessageResponse
from typing import List, Optional

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/dialogs", response_model=List[DialogResponse])
async def get_dialogs(
    status: Optional[str] = Query(None, description="active, completed"),
    campaign_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Список диалогов с фильтрацией."""
    service = LogsService(db)
    return await service.get_dialogs(status=status, campaign_id=campaign_id, limit=limit, offset=offset)


@router.get("/dialogs/{dialog_id}", response_model=DialogResponse)
async def get_dialog_detail(dialog_id: int, db: AsyncSession = Depends(get_db)):
    """Детальная информация о диалоге."""
    service = LogsService(db)
    dialog = await service.get_dialog_detail(dialog_id)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    return dialog


@router.get("/dialogs/{dialog_id}/messages", response_model=List[MessageResponse])
async def get_dialog_messages(dialog_id: int, db: AsyncSession = Depends(get_db)):
    """Все сообщения в диалоге (история переписки)."""
    service = LogsService(db)
    return await service.get_dialog_messages(dialog_id)