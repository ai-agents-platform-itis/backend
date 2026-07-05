from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.campaign import CampaignRepository
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.models.campaign import Campaign


class CampaignService:
    def __init__(self, session: AsyncSession):
        self.repo = CampaignRepository(session)

    async def create_campaign(self, data: CampaignCreate) -> Campaign:
        # Тут может быть дополнительная логика:
        # - проверка уникальности названия
        # - валидация niche_type
        # - установка дефолтного промпта
        return await self.repo.create(**data.model_dump())

    async def get_all_campaigns(self) -> Sequence[Campaign]:
        return await self.repo.get_all()

    async def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        return await self.repo.get_by_id(campaign_id)

    async def update_campaign(self, campaign_id: int, data: CampaignUpdate) -> Campaign:
        campaign = await self.repo.get_by_id(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        return await self.repo.update(campaign, **data.model_dump(exclude_unset=True))

    async def delete_campaign(self, campaign_id: int) -> None:
        campaign = await self.repo.get_by_id(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        await self.repo.delete(campaign)