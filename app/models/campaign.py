from sqlalchemy import String, Boolean, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import datetime


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    niche_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # "plots", "gambling", "services"
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    welcome_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    rag_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    leads = relationship("Lead", back_populates="campaign")
    dialogs = relationship("Dialog", back_populates="campaign")
    knowledge_docs = relationship("KnowledgeDoc", back_populates="campaign")  # ← новое

    def __repr__(self):
        return (
            f"<Campaign(id={self.id}, name='{self.name}', niche='{self.niche_type}')>"
        )
