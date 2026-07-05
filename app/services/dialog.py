from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.dialog import DialogRepository
from app.schemas.dialog import DialogCreate, MessageCreate
from app.models.dialog import Dialog
from app.models.message import Message


class DialogService:
    def __init__(self, session: AsyncSession):
        self.repo = DialogRepository(session)

    async def create_dialog(self, data: DialogCreate) -> Dialog:
        return await self.repo.create(**data.model_dump())

    async def get_all_dialogs(self) -> Sequence[Dialog]:
        return await self.repo.get_all()

    async def get_dialog(self, dialog_id: int) -> Optional[Dialog]:
        return await self.repo.get_by_id(dialog_id)

    async def add_message(self, dialog_id: int, data: MessageCreate) -> Message:
        dialog = await self.repo.get_by_id(dialog_id)
        if not dialog:
            raise ValueError("Dialog not found")
        return await self.repo.add_message(dialog_id, data.role, data.content)

    async def get_messages(self, dialog_id: int) -> Sequence[Message]:
        dialog = await self.repo.get_by_id(dialog_id)
        if not dialog:
            raise ValueError("Dialog not found")
        return await self.repo.get_messages(dialog_id)