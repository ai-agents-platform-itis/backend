from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.stats import StatsService
from typing import Optional

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    """Общая статистика по всей системе."""
    service = StatsService(db)
    return await service.get_overview()


@router.get("/campaigns/{campaign_id}")
async def get_campaign_stats(campaign_id: int, db: AsyncSession = Depends(get_db)):
    """Статистика по конкретной кампании."""
    service = StatsService(db)
    return await service.get_campaign_stats(campaign_id)


@router.get("/leads")
async def get_leads_stats(
    status: Optional[str] = Query(None, description="new, qualified, hot, closed"),
    db: AsyncSession = Depends(get_db)
):
    """Статистика по лидам с фильтрацией по статусу."""
    service = StatsService(db)
    return await service.get_leads_stats(status)