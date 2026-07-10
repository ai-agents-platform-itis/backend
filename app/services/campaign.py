from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.campaign import CampaignRepository
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.models.campaign import Campaign

DEFAULT_PRESETS = {
    "plots": {
        "system_prompt": "Ты — агент по продаже земельных участков. Твоя задача — помочь клиенту выбрать подходящий участок, ответить на вопросы о цене, расположении, документах. Будь вежлив, профессионален, используй информацию из базы знаний.",
        "welcome_message": "Здравствуйте! Интересуетесь покупкой земельного участка? Я помогу подобрать лучший вариант под ваш бюджет и пожелания. Расскажите, что вы ищете?",
    },
    "gambling": {
        "system_prompt": "Ты — агент по привлечению игроков в онлайн-казино. Твоя задача — заинтересовать клиента бонусами, акциями, рассказать об играх. Будь энергичен, но не навязчив. Не давай ложных обещаний.",
        "welcome_message": "Привет! Готов испытать удачу? У нас сейчас крутые бонусы для новых игроков — фриспины и кэшбек. Что тебе интересно: слоты, покер, рулетка?",
    },
    "services": {
        "system_prompt": "Ты — агент по продаже услуг. Твоя задача — понять потребность клиента, предложить подходящую услугу, объяснить преимущества и цену. Будь дружелюбен, консультируй, помогай с выбором.",
        "welcome_message": "Добрый день! Какие услуги вас интересуют? Я помогу подобрать оптимальное решение, расскажу про цены и условия.",
    },
}

class CampaignService:
    def __init__(self, session: AsyncSession):
        self.repo = CampaignRepository(session)

    async def create_campaign(self, data: CampaignCreate) -> Campaign:
        preset = DEFAULT_PRESETS.get(data.niche_type, {})
        if not data.system_prompt:
            data.system_prompt = preset.get("system_prompt")
        if not data.welcome_message:
            data.welcome_message = preset.get("welcome_message")
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