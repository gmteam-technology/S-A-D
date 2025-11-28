from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SoilSample
from app.schemas import SoilAnalysisResponse, SoilSampleSchema


class SoilService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_sample(self, payload: SoilSampleSchema) -> SoilSampleSchema:
        sample = SoilSample(**payload.model_dump())
        self.db.add(sample)
        await self.db.commit()
        await self.db.refresh(sample)
        return SoilSampleSchema.model_validate(sample)

    async def analyze(self, field_id: int) -> SoilAnalysisResponse:
        stmt = select(SoilSample).where(SoilSample.field_id == field_id)
        samples = (await self.db.execute(stmt)).scalars().all()
        if not samples:
            return SoilAnalysisResponse(field_id=field_id, lime_recommendation_kg_ha=0, fertilizer_plan={}, warnings=["Sem dados"])
        avg_ph = sum(s.ph for s in samples) / len(samples)
        lime = max(0, (6.2 - avg_ph) * 250)
        fertilizer_plan = {
            "N": round(sum(s.nitrogen for s in samples) / len(samples) * 1.2, 2),
            "P": round(sum(s.phosphorus for s in samples) / len(samples) * 0.8, 2),
            "K": round(sum(s.potassium for s in samples) / len(samples) * 0.6, 2),
        }
        warnings = []
        if avg_ph < 5.5:
            warnings.append("pH abaixo do ideal, sugerir calcário")
        return SoilAnalysisResponse(
            field_id=field_id,
            lime_recommendation_kg_ha=round(lime, 2),
            fertilizer_plan=fertilizer_plan,
            warnings=warnings,
        )
