from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DialogCreate(BaseModel):
    lead_id: int
    campaign_id: int


class MessageCreate(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    id: int
    dialog_id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class DialogResponse(BaseModel):
    id: int
    lead_id: int
    campaign_id: int
    status: str
    started_at: datetime
    finished_at: Optional[datetime]

    class Config:
        from_attributes = True