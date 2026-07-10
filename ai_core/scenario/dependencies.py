import os
from functools import lru_cache

from .ollama_client import OllamaClient
from .scenario_master import ScenarioMaster


@lru_cache(maxsize=1)
def get_llm_client():
    return OllamaClient(
        os.getenv("OLLAMA_SCENARIO_MODEL"), base_url=os.getenv("OLLAMA_BASE_URL")
    )


@lru_cache(maxsize=1)
def get_scenario_master():
    _llm_client = get_llm_client()
    _scenario_master = ScenarioMaster(llm_client=_llm_client)

    return _scenario_master
