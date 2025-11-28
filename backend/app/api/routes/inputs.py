from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas import CostAnalysisSchema, CostComparisonResponse, InputItemSchema
from app.services.inputs import InputService

router = APIRouter()


@router.get("", response_model=list[InputItemSchema])
async def list_inputs(db: AsyncSession = Depends(get_db)) -> list[InputItemSchema]:
    return await InputService(db).list_items()


@router.post("", response_model=InputItemSchema)
async def create_input(payload: InputItemSchema, db: AsyncSession = Depends(get_db)) -> InputItemSchema:
    return await InputService(db).create_item(payload)


@router.post("/cost-analysis", response_model=CostComparisonResponse)
async def analyze_cost(payload: CostAnalysisSchema, db: AsyncSession = Depends(get_db)) -> CostComparisonResponse:
    return await InputService(db).analyze_cost(payload)
