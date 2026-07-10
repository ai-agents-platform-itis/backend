from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("idx_leads_campaign_id", "campaign_id"),
        Index("idx_leads_status", "status"),
        Index("idx_leads_campaign_status", "campaign_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaigns.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # "instagram", "avito"
    contact: Mapped[str] = mapped_column(String(255), nullable=False)  # @username или телефон
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # Вся спарсенная инфа
    status: Mapped[str] = mapped_column(String(20), default="new")  # new, qualified, hot, closed
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    campaign = relationship("Campaign", back_populates="leads")
    dialogs = relationship("Dialog", back_populates="lead")

    def __repr__(self):
        return f"<Lead(id={self.id}, source='{self.source}', contact='{self.contact}', status='{self.status}')>"