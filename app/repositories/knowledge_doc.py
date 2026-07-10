from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Optional
from app.models.knowledge_doc import KnowledgeDoc
from app.repositories.base import BaseRepository


class KnowledgeDocRepository(BaseRepository[KnowledgeDoc]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=KnowledgeDoc, session=session)

    async def get_by_campaign_id(self, campaign_id: int) -> Sequence[KnowledgeDoc]:
        result = await self.session.execute(
            select(KnowledgeDoc).where(KnowledgeDoc.campaign_id == campaign_id)
        )
        return result.scalars().all()

    async def get_with_content(self, doc_id: int) -> Optional[KnowledgeDoc]:
        """Получить документ с текстом (для ChromaDB)."""
        result = await self.session.execute(
            select(KnowledgeDoc).where(KnowledgeDoc.id == doc_id)
        )
        return result.scalar_one_or_none()