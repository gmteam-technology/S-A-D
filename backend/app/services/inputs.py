from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InputCostAnalysis, InputItem
from app.schemas import CostAnalysisSchema, CostComparisonResponse, InputItemSchema


class InputService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self) -> list[InputItemSchema]:
        result = await self.db.execute(select(InputItem))
        return [InputItemSchema.model_validate(item) for item in result.scalars().all()]

    async def create_item(self, payload: InputItemSchema) -> InputItemSchema:
        item = InputItem(**payload.model_dump(exclude_none=True))
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return InputItemSchema.model_validate(item)

    async def analyze_cost(self, payload: CostAnalysisSchema) -> CostComparisonResponse:
        baseline = await self.db.execute(
            select(InputCostAnalysis).where(InputCostAnalysis.field_id == payload.field_id).order_by(InputCostAnalysis.created_at.desc())
        )
        baseline_cost = baseline.scalars().first()
        baseline_value = float(baseline_cost.cost_per_ha) if baseline_cost else payload.cost_per_ha
        scenario_cost = payload.cost_per_ha * (1 + payload.delta_price_pct / 100)
        sensitivity = {
            "fertilizantes": payload.delta_price_pct * 0.4,
            "defensivos": payload.delta_price_pct * 0.35,
            "sementes": payload.delta_price_pct * 0.25,
        }
        analysis = InputCostAnalysis(**payload.model_dump())
        self.db.add(analysis)
        await self.db.commit()
        return CostComparisonResponse(
            baseline_cost=baseline_value,
            scenario_cost=round(scenario_cost, 2),
            sensitivity=sensitivity,
        )
