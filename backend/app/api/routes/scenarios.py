from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User
from app.schemas import ScenarioEvaluationSchema, ScenarioSchema
from app.services.scenarios import ScenarioService

router = APIRouter()


@router.post("", response_model=ScenarioSchema)
async def create_scenario(
    payload: ScenarioSchema,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> ScenarioSchema:
    service = ScenarioService(db)
    return await service.create(current_user.id, payload)


@router.post("/{scenario_id}/evaluate", response_model=ScenarioEvaluationSchema)
async def evaluate_scenario(scenario_id: int, db: AsyncSession = Depends(deps.get_db)) -> ScenarioEvaluationSchema:
    service = ScenarioService(db)
    return await service.evaluate(scenario_id)


@router.post("/compare", response_model=list[ScenarioEvaluationSchema])
async def compare(payload: list[int], db: AsyncSession = Depends(deps.get_db)) -> list[ScenarioEvaluationSchema]:
    service = ScenarioService(db)
    return await service.compare(payload)
