from sqlalchemy import String, Integer, DateTime, func, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime


class Dialog(Base):
    __tablename__ = "dialogs"
    __table_args__ = (
        Index("idx_dialogs_campaign_id", "campaign_id"),
        Index("idx_dialogs_lead_id", "lead_id"),
        Index("idx_dialogs_status", "status"),
        Index("idx_dialogs_campaign_status", "campaign_id", "status"),
        Index("idx_dialogs_started_at", "started_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"), nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaigns.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    campaign = relationship("Campaign", back_populates="dialogs")
    lead = relationship("Lead", back_populates="dialogs")


    def __repr__(self):
        return f"<Dialog(id={self.id}, lead_id={self.lead_id}, status='{self.status}')>"