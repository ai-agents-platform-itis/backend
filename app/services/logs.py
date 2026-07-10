from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dialog import Dialog
from app.models.message import Message


class LogsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dialogs(
        self,
        status: Optional[str] = None,
        campaign_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Dialog]:
        query = select(Dialog)
        if status:
            query = query.where(Dialog.status == status)
        if campaign_id:
            query = query.where(Dialog.campaign_id == campaign_id)
        query = query.order_by(Dialog.started_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_dialog_messages(self, dialog_id: int) -> Sequence[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.dialog_id == dialog_id)
            .order_by(Message.timestamp)
        )
        return result.scalars().all()

    async def get_dialog_detail(self, dialog_id: int) -> Optional[Dialog]:
        result = await self.session.execute(
            select(Dialog).where(Dialog.id == dialog_id)
        )
        return result.scalar_one_or_none()