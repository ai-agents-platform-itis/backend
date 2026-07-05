from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.dialog import DialogService
from app.schemas.dialog import DialogCreate, DialogResponse, MessageCreate, MessageResponse
from typing import List

router = APIRouter(prefix="/dialogs", tags=["Dialogs"])


@router.post("/", response_model=DialogResponse, status_code=status.HTTP_201_CREATED)
async def create_dialog(data: DialogCreate, db: AsyncSession = Depends(get_db)):
    service = DialogService(db)
    return await service.create_dialog(data)


@router.get("/", response_model=List[DialogResponse])
async def list_dialogs(db: AsyncSession = Depends(get_db)):
    service = DialogService(db)
    return await service.get_all_dialogs()


@router.get("/{dialog_id}", response_model=DialogResponse)
async def get_dialog(dialog_id: int, db: AsyncSession = Depends(get_db)):
    service = DialogService(db)
    dialog = await service.get_dialog(dialog_id)
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    return dialog


@router.post("/{dialog_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def add_message(dialog_id: int, data: MessageCreate, db: AsyncSession = Depends(get_db)):
    service = DialogService(db)
    try:
        return await service.add_message(dialog_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{dialog_id}/messages", response_model=List[MessageResponse])
async def get_messages(dialog_id: int, db: AsyncSession = Depends(get_db)):
    service = DialogService(db)
    try:
        return await service.get_messages(dialog_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))