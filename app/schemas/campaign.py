from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    niche_type: str = Field(..., pattern="^(plots|gambling|services)$")  # только эти три ниши
    system_prompt: Optional[str] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    niche_type: Optional[str] = Field(None, pattern="^(plots|gambling|services)$")
    system_prompt: Optional[str] = None
    is_active: Optional[bool] = None


class CampaignResponse(BaseModel):
    id: int
    name: str
    niche_type: str
    system_prompt: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Чтобы работало с SQLAlchemy моделями