from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.dialog import Dialog
from app.models.message import Message
from app.repositories.base import BaseRepository


class DialogRepository(BaseRepository[Dialog]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Dialog, session=session)

    async def get_messages(self, dialog_id: int) -> Sequence[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.dialog_id == dialog_id)
            .order_by(Message.timestamp)
        )
        return result.scalars().all()

    async def add_message(self, dialog_id: int, role: str, content: str) -> Message:
        message = Message(dialog_id=dialog_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message