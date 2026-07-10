from ollama import AsyncClient


class OllamaClient:
    def __init__(self, model_name: str = "qwen3.5:9b", base_url: str = None):
        self.model_name = model_name
        self.base_url = base_url or "http://localhost:11434"
        self.client = AsyncClient(host=self.base_url)

    async def chat(self, messages: list, temperature: float = 0.5) -> dict:
        response = await self.client.chat(
            model=self.model_name,
            messages=messages,
            options={"temperature": temperature, "num_ctx": 8192, "num_predict": 4096},
            format="json",
            stream=False,
            think=False,
        )
        return response
