from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.campaign import CampaignService
from app.services.knowledge_doc import KnowledgeDocService
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.schemas.knowledge_doc import KnowledgeDocResponse
from typing import List

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(data: CampaignCreate, db: AsyncSession = Depends(get_db)):
    service = CampaignService(db)
    return await service.create_campaign(data)


@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    service = CampaignService(db)
    return await service.get_all_campaigns()


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    service = CampaignService(db)
    campaign = await service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(campaign_id: int, data: CampaignUpdate, db: AsyncSession = Depends(get_db)):
    service = CampaignService(db)
    try:
        return await service.update_campaign(campaign_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    service = CampaignService(db)
    try:
        await service.delete_campaign(campaign_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

# ==================== Knowledge Docs ====================

@router.post("/{campaign_id}/knowledge", response_model=KnowledgeDocResponse, status_code=status.HTTP_201_CREATED)
async def upload_knowledge(
    campaign_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Загрузить PDF/TXT/MD документ для базы знаний кампании."""
    service = KnowledgeDocService(db)
    return await service.upload_document(campaign_id, file)


@router.get("/{campaign_id}/knowledge", response_model=List[KnowledgeDocResponse])
async def get_campaign_knowledge(campaign_id: int, db: AsyncSession = Depends(get_db)):
    """Получить список всех документов кампании."""
    service = KnowledgeDocService(db)
    return await service.get_campaign_documents(campaign_id)