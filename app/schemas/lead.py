from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any


class LeadCreate(BaseModel):
    campaign_id: int
    source: str = Field(..., pattern="^(instagram|avito)$")
    contact: str = Field(..., min_length=1)
    raw_data: Optional[dict] = None


class LeadResponse(BaseModel):
    id: int
    campaign_id: int
    source: str
    contact: str
    raw_data: Optional[dict]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True