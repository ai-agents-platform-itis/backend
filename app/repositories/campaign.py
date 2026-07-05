from sqlalchemy.ext.asyncio import AsyncSession
from app.models.campaign import Campaign
from app.repositories.base import BaseRepository


class CampaignRepository(BaseRepository[Campaign]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Campaign, session=session)