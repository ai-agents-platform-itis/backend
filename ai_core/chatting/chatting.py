import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from rag import DocumentStore, get_document_store

with open("prompts/CHATTING.md") as f:
    CHATTING_PROMPT = f.read()


class Chatting:
    def __init__(self):
        self.store: DocumentStore = get_document_store()
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_CHAT_MODEL"),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            ),
            temperature=0,
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CHATTING_PROMPT),
                ("human", "{question}"),
            ]
        )

    async def answer_question(self, campaign_id: int, query: str, limit=5) -> str:
        documents = self.store.search(campaign_id=campaign_id, query=query, limit=limit)

        if not documents:
            return {"answer": "В базе знаний нет информации для ответа."}

        context = "\n\n".join(
            (
                f"[Фрагмент {index}]\n"
                f"Файл: {document.metadata.get('filename')}\n"
                f"{document.page_content}"
            )
            for index, document in enumerate(documents, start=1)
        )

        messages = self.prompt.invoke(
            {
                "context": context,
                "question": query,
            }
        )

        resp = await self.llm.ainvoke(messages)
        return resp["content"]
