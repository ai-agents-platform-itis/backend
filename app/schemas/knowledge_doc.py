from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class KnowledgeDocResponse(BaseModel):
    id: int
    campaign_id: int
    filename: str
    file_path: str
    content_text: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True