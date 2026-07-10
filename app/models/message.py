from sqlalchemy import String, Integer, DateTime, Text, func, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import datetime


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_dialog_id", "dialog_id"),
        Index("idx_messages_timestamp", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dialog_id: Mapped[int] = mapped_column(Integer, ForeignKey("dialogs.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # "user", "assistant", "system"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"<Message(id={self.id}, dialog_id={self.dialog_id}, role='{self.role}')>"