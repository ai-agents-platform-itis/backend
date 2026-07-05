from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import datetime


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaigns.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # "instagram", "avito"
    contact: Mapped[str] = mapped_column(String(255), nullable=False)  # @username или телефон
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # Вся спарсенная инфа
    status: Mapped[str] = mapped_column(String(20), default="new")  # new, qualified, hot, closed
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"<Lead(id={self.id}, source='{self.source}', contact='{self.contact}', status='{self.status}')>"