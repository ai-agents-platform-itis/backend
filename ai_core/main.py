from ollama_client import OllamaClient
from ai_scenario import generate_scenario


llm_client = OllamaClient(model_name="qwen3.5:9b", base_url="http://localhost:11434")


async def main():
    result = await generate_scenario(llm_client, topic="Как приготовить пиццу", duration_sec=60, style="динамичный образовательный ролик", temperature=0.5)
    print(result)
    with open("scenario.json", "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=4, ensure_ascii=False))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())