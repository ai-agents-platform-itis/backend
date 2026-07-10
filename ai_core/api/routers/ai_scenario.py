from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from scenario import ScenarioMaster, get_scenario_master

router = APIRouter(prefix="/ai", tags=["AI"])


ScenarioMasterDep = Annotated[ScenarioMaster, Depends(get_scenario_master)]


class ScenarioCreate(BaseModel):
    topic: str
    duration_sec: int
    style: str
    temperature: float = 0.5


@router.post("/generate_scenario")
async def generate_scenario_endpoint(
    scenario_master: ScenarioMasterDep, payload: ScenarioCreate
):
    scenario = await scenario_master.generate_scenario(
        topic=payload.topic,
        duration_sec=payload.duration_sec,
        style=payload.style,
        temperature=payload.temperature,
    )
    return scenario.model_dump()
