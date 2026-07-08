from fastapi import APIRouter, FastAPI, Query
from ai_scenario import generate_scenario
from ollama_client import OllamaClient
import os
from dotenv import load_dotenv


load_dotenv()


router = APIRouter(prefix="/ai", tags=["AI"])
llm_client = OllamaClient(model_name=os.getenv("OLLAMA_MODEL"), base_url=os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434")


@router.get("/generate_scenario")
async def generate_scenario_endpoint(topic: str = Query(..., description="Тема видео"), duration_sec: int = Query(..., description="Длительность видео в секундах"), style: str = Query(..., description="Стиль видео"), temperature: float = Query(0.5, description="Температура генерации")):
    scenario = await generate_scenario(llm_client, topic, duration_sec, style, temperature)
    return scenario.model_dump()

