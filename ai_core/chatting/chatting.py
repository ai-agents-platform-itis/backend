import json
import os
from pathlib import Path
from typing import Any, Literal, TypedDict

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from ai_core.rag import DocumentStore, get_document_store


AI_CORE_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = AI_CORE_DIR / "prompts"

with open(PROMPTS_DIR / "CHATTING.md") as f:
    CHATTING_PROMPT = f.read()

with open(PROMPTS_DIR / "CRITIC.md") as f:
    CRITIC_PROMPT = f.read()

with open(PROMPTS_DIR / "QUALIFIER.md") as f:
    QUALIFIER_PROMPT = f.read()



LeadLevel = Literal["hot", "warm", "cold"]
CriticVerdict = Literal["ok", "hallucination", "insufficient_context"]


class ChattingState(TypedDict, total=False):
    campaign_id: int
    query: str
    limit: int

    documents: list[Document]
    context: str
    answer: str

    lead_level: LeadLevel
    lead_reason: str
    next_action: str

    critic_verdict: CriticVerdict
    critic_notes: str

    sources: list[dict[str, Any]]


class Chatting:
    def __init__(self):
        self.store: DocumentStore = get_document_store()

        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_CHAT_MODEL"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0,
        )

        self.sales_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CHATTING_PROMPT),
                ("human", "{question}"),
            ]
        )

        self.qualifier_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    QUALIFIER_PROMPT,
                ),
                ("human", "{question}"),
            ]
        )

        self.critic_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    CRITIC_PROMPT,
                ),
                (
                    "human",
                    """
Контекст:
{context}

Вопрос пользователя:
{question}

Ответ ассистента:
{answer}
""",
                ),
            ]
        )

        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(ChattingState)

        graph.add_node("retrieve_context", self._retrieve_context)
        graph.add_node("sales_answer", self._sales_answer)
        graph.add_node("qualify_lead", self._qualify_lead)
        graph.add_node("critic_check", self._critic_check)

        graph.set_entry_point("retrieve_context")
        graph.add_edge("retrieve_context", "sales_answer")
        graph.add_edge("sales_answer", "qualify_lead")
        graph.add_edge("qualify_lead", "critic_check")
        graph.add_edge("critic_check", END)

        return graph.compile()

    async def answer_question(
        self,
        campaign_id: int,
        query: str,
        limit: int = 5,
    ) -> dict[str, Any]:
        state = await self.graph.ainvoke(
            {
                "campaign_id": campaign_id,
                "query": query,
                "limit": limit,
            }
        )

        return {
            "answer": state.get("answer"),
            "lead": {
                "level": state.get("lead_level"),
                "reason": state.get("lead_reason"),
                "next_action": state.get("next_action"),
            },
            "critic": {
                "verdict": state.get("critic_verdict"),
                "notes": state.get("critic_notes"),
            },
            "sources": state.get("sources", []),
        }

    async def _retrieve_context(self, state: ChattingState) -> ChattingState:
        documents = self.store.search(
            campaign_id=state["campaign_id"],
            query=state["query"],
            limit=state["limit"],
        )

        context = "\n\n".join(
            (
                f"[Фрагмент {index}]\n"
                f"Файл: {document.metadata.get('filename')}\n"
                f"{document.page_content}"
            )
            for index, document in enumerate(documents, start=1)
        )

        sources = [
            {
                "filename": document.metadata.get("filename"),
                "document_id": document.metadata.get("document_id"),
                "chunk_index": document.metadata.get("chunk_index"),
            }
            for document in documents
        ]

        return {
            "documents": documents,
            "context": context,
            "sources": sources,
        }

    async def _sales_answer(self, state: ChattingState) -> ChattingState:
        if not state.get("documents"):
            return {
                "answer": "В базе знаний нет информации для ответа.",
            }

        messages = self.sales_prompt.invoke(
            {
                "context": state["context"],
                "question": state["query"],
            }
        )

        response = await self.llm.ainvoke(messages)

        return {
            "answer": response.content,
        }

    async def _qualify_lead(self, state: ChattingState) -> ChattingState:
        messages = self.qualifier_prompt.invoke(
            {
                "question": state["query"],
            }
        )

        response = await self.llm.ainvoke(messages)
        data = self._parse_json(response.content)

        lead_level = data.get("lead_level", "cold")

        if lead_level not in {"hot", "warm", "cold"}:
            lead_level = "cold"

        return {
            "lead_level": lead_level,
            "lead_reason": data.get("reason", "Причина не определена."),
            "next_action": data.get(
                "next_action",
                "Продолжить диалог и уточнить потребность пользователя.",
            ),
        }

    async def _critic_check(self, state: ChattingState) -> ChattingState:
        if not state.get("context"):
            return {
                "critic_verdict": "insufficient_context",
                "critic_notes": "Релевантный контекст не найден.",
            }

        messages = self.critic_prompt.invoke(
            {
                "context": state["context"],
                "question": state["query"],
                "answer": state["answer"],
            }
        )

        response = await self.llm.ainvoke(messages)
        data = self._parse_json(response.content)

        verdict = data.get("verdict", "insufficient_context")

        if verdict not in {"ok", "hallucination", "insufficient_context"}:
            verdict = "insufficient_context"

        return {
            "critic_verdict": verdict,
            "critic_notes": data.get("notes", "Критик не вернул пояснение."),
        }

    @staticmethod
    def _parse_json(value: str) -> dict[str, Any]:
        value = value.strip()

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            start = value.find("{")
            end = value.rfind("}")

            if start == -1 or end == -1 or end <= start:
                return {}

            try:
                return json.loads(value[start : end + 1])
            except json.JSONDecodeError:
                return {}