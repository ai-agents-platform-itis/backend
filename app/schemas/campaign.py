from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    niche_type: str = Field(..., pattern="^(plots|gambling|services)$")
    system_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    rag_enabled: bool = False


class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    niche_type: Optional[str] = Field(None, pattern="^(plots|gambling|services)$")
    system_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    rag_enabled: Optional[bool] = None
    is_active: Optional[bool] = None


class CampaignResponse(BaseModel):
    id: int
    name: str
    niche_type: str
    system_prompt: Optional[str]
    welcome_message: Optional[str]
    rag_enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True