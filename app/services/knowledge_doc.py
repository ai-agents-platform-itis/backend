import os
import uuid
from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status
from app.repositories.knowledge_doc import KnowledgeDocRepository
from app.models.knowledge_doc import KnowledgeDoc

UPLOAD_DIR = "uploads/knowledge"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


class KnowledgeDocService:
    def __init__(self, session: AsyncSession):
        self.repo = KnowledgeDocRepository(session)

    async def upload_document(self, campaign_id: int, file: UploadFile) -> KnowledgeDoc:
        # Проверка расширения
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Недопустимый формат файла. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Создаём папку, если нет
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Генерируем уникальное имя файла
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        # Сохраняем файл на диск
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # Пытаемся извлечь текст
        text_content = None
        if ext == ".pdf":
            text_content = self._extract_pdf_text(content)
        elif ext in {".txt", ".md"}:
            text_content = content.decode("utf-8", errors="ignore")

        return await self.repo.create(
            campaign_id=campaign_id,
            filename=file.filename or "unknown",
            file_path=file_path,
            content_text=text_content,
        )

    def _extract_pdf_text(self, content: bytes) -> Optional[str]:
        """Извлечение текста из PDF. Пока заглушка, потом подключим PyPDF2."""
        try:
            from PyPDF2 import PdfReader
            import io
            reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip() or None
        except ImportError:
            # PyPDF2 не установлен — вернём None, текст можно извлечь позже
            return None
        except Exception:
            return None

    async def get_campaign_documents(self, campaign_id: int) -> Sequence[KnowledgeDoc]:
        return await self.repo.get_by_campaign_id(campaign_id)

    async def get_document_content(self, doc_id: int) -> Optional[KnowledgeDoc]:
        doc = await self.repo.get_with_content(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Документ не найден")
        return doc