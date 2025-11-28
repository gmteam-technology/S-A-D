from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas import SoilAnalysisResponse, SoilSampleSchema
from app.services.soil import SoilService

router = APIRouter()


@router.post("/samples", response_model=SoilSampleSchema)
async def create_sample(payload: SoilSampleSchema, db: AsyncSession = Depends(get_db)) -> SoilSampleSchema:
    service = SoilService(db)
    return await service.create_sample(payload)


@router.get("/analysis", response_model=SoilAnalysisResponse)
async def analyze(field_id: int, db: AsyncSession = Depends(get_db)) -> SoilAnalysisResponse:
    service = SoilService(db)
    return await service.analyze(field_id)
