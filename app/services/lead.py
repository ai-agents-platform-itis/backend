from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.lead import LeadRepository
from app.schemas.lead import LeadCreate
from app.models.lead import Lead


class LeadService:
    def __init__(self, session: AsyncSession):
        self.repo = LeadRepository(session)

    async def create_lead(self, data: LeadCreate) -> Lead:
        return await self.repo.create(**data.model_dump())

    async def get_leads(self, status: Optional[str] = None) -> Sequence[Lead]:
        if status:
            return await self.repo.get_by_status(status)
        return await self.repo.get_all()

    async def get_lead(self, lead_id: int) -> Optional[Lead]:
        return await self.repo.get_by_id(lead_id)