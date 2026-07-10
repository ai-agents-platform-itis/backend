from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.dialog import Dialog
from app.models.lead import Lead
from app.models.campaign import Campaign


class StatsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_overview(self) -> dict:
        # Всего диалогов
        total_dialogs = await self.session.scalar(
            select(func.count(Dialog.id))
        )
        # Активные
        active_dialogs = await self.session.scalar(
            select(func.count(Dialog.id)).where(Dialog.status == "active")
        )
        # Завершённые
        completed_dialogs = await self.session.scalar(
            select(func.count(Dialog.id)).where(Dialog.status == "completed")
        )
        # Всего лидов
        total_leads = await self.session.scalar(
            select(func.count(Lead.id))
        )
        # Новые лиды
        new_leads = await self.session.scalar(
            select(func.count(Lead.id)).where(Lead.status == "new")
        )
        # Горячие лиды
        hot_leads = await self.session.scalar(
            select(func.count(Lead.id)).where(Lead.status == "hot")
        )
        # Всего кампаний
        total_campaigns = await self.session.scalar(
            select(func.count(Campaign.id))
        )
        # Активные кампании
        active_campaigns = await self.session.scalar(
            select(func.count(Campaign.id)).where(Campaign.is_active == True)
        )

        return {
            "dialogs": {
                "total": total_dialogs,
                "active": active_dialogs,
                "completed": completed_dialogs,
            },
            "leads": {
                "total": total_leads,
                "new": new_leads,
                "hot": hot_leads,
            },
            "campaigns": {
                "total": total_campaigns,
                "active": active_campaigns,
            },
        }

    async def get_campaign_stats(self, campaign_id: int) -> dict:
        # Диалоги по кампании
        total_dialogs = await self.session.scalar(
            select(func.count(Dialog.id)).where(Dialog.campaign_id == campaign_id)
        )
        active_dialogs = await self.session.scalar(
            select(func.count(Dialog.id)).where(
                Dialog.campaign_id == campaign_id,
                Dialog.status == "active"
            )
        )
        completed_dialogs = await self.session.scalar(
            select(func.count(Dialog.id)).where(
                Dialog.campaign_id == campaign_id,
                Dialog.status == "completed"
            )
        )
        # Лиды по кампании
        total_leads = await self.session.scalar(
            select(func.count(Lead.id)).where(Lead.campaign_id == campaign_id)
        )
        new_leads = await self.session.scalar(
            select(func.count(Lead.id)).where(
                Lead.campaign_id == campaign_id,
                Lead.status == "new"
            )
        )
        hot_leads = await self.session.scalar(
            select(func.count(Lead.id)).where(
                Lead.campaign_id == campaign_id,
                Lead.status == "hot"
            )
        )

        return {
            "campaign_id": campaign_id,
            "dialogs": {
                "total": total_dialogs,
                "active": active_dialogs,
                "completed": completed_dialogs,
            },
            "leads": {
                "total": total_leads,
                "new": new_leads,
                "hot": hot_leads,
            },
        }

    async def get_leads_stats(self, status: str = None) -> list:
        query = select(Lead)
        if status:
            query = query.where(Lead.status == status)
        result = await self.session.execute(query)
        return result.scalars().all()