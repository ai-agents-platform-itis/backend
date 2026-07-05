from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lead import Lead
from app.repositories.base import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Lead, session=session)

    async def get_by_status(self, status: str) -> Sequence[Lead]:
        result = await self.session.execute(
            select(Lead).where(Lead.status == status)
        )
        return result.scalars().all()