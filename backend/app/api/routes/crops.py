from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas import (
    ProductivitySchema,
    SeasonSchema,
    SimulationCompareRequest,
    SimulationRequest,
    SimulationResult,
)
from app.services.crops import CropService

router = APIRouter()


@router.get("/season", response_model=list[SeasonSchema])
async def list_seasons(db: AsyncSession = Depends(get_db)) -> list[SeasonSchema]:
    service = CropService(db)
    return await service.list_seasons()


@router.get("/productivity", response_model=list[ProductivitySchema])
async def list_productivity(season_id: int, db: AsyncSession = Depends(get_db)) -> list[ProductivitySchema]:
    service = CropService(db)
    return await service.list_productivity(season_id)


@router.post("/simulation", response_model=SimulationResult)
async def run_simulation(payload: SimulationRequest, db: AsyncSession = Depends(get_db)) -> SimulationResult:
    service = CropService(db)
    return await service.run_simulation(payload)


@router.post("/simulation/compare", response_model=list[SimulationResult])
async def compare_simulations(payload: SimulationCompareRequest, db: AsyncSession = Depends(get_db)) -> list[SimulationResult]:
    service = CropService(db)
    return await service.compare(payload)
