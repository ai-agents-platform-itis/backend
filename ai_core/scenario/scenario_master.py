import json
import logging
from pathlib import Path

from pydantic import ValidationError

from .models import Scenario

logger = logging.getLogger("ai_scenario")

AI_CORE_DIR = Path(__file__).resolve().parents[1]
PROMPTS_DIR = AI_CORE_DIR / "prompts"


def load_scenario_meta_prompt() -> str:
    with open(PROMPTS_DIR / "AI_SCENARIO.md", "r", encoding="utf-8") as f:
        return f.read()


SCENARIO_META_PROMPT = load_scenario_meta_prompt()


class ScenarioMaster:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    @staticmethod
    def build_user_prompt(
        topic: str, duration_sec: int, style: str, audience: str
    ) -> str:
        return f"""/no_think


    Создай JSON-сценарий видео.
    Сгенерируй сценарий на русском языке.

    Важно:
    - Русский язык использовать только для title, voice_over.text и caption.text.
    - Английский использовать только для visual.query и visual.fallback_image_prompt.
    - Не переводи voice_over.text и caption.text на английский.

    Тема: {topic}
    Длительность: ~{duration_sec} секунд
    Аудитория: {audience}
    Стиль: {style}

    Сделай сцены по 5-10 секунд.
    """

    @staticmethod
    def parse_scenario(raw_text: str) -> Scenario:
        data = json.loads(raw_text)
        return Scenario.model_validate(data)

    async def generate_scenario(
        self, topic: str, duration_sec: int, style: str, temperature: float
    ) -> Scenario:
        messages = [
            {"role": "system", "content": SCENARIO_META_PROMPT},
            {
                "role": "user",
                "content": self.build_user_prompt(
                    topic=topic,
                    duration_sec=duration_sec,
                    audience="широкая аудитория",
                    style=style,
                ),
            },
        ]
        logger.info(f"Sending request to LLM with messages: {messages}")
        raw = await self.llm_client.chat(messages, temperature=temperature)

        json_text = json.dumps(
            raw.model_dump(),
            ensure_ascii=False,
            indent=2,
        )
        logger.info(f"Response from LLM:\n{json_text}")

        content = raw["message"]["content"]

        try:
            return self.parse_scenario(content)
        except (json.JSONDecodeError, ValidationError) as error:
            logger.error(f"Error parsing scenario: {error}. Attempting to repair JSON.")
            repair_messages = [
                {"role": "system", "content": SCENARIO_META_PROMPT},
                {
                    "role": "user",
                    "content": f"""
    JSON ниже не прошел валидацию.

    Ошибка:
    {str(error)}

    Исправь JSON. Верни только исправленный JSON.

    Исходный ответ:
    {content}
    """,
                },
            ]

            repaired = await self.llm_client.chat(repair_messages)
            logger.info(
                "Repaired response from LLM:\n"
                + f"{json.dumps(repaired.model_dump(), ensure_ascii=False, indent=2)}"
            )
            return self.parse_scenario(repaired["message"]["content"])
