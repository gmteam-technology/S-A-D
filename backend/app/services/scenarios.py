from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Scenario, ScenarioEvaluation
from app.schemas import ScenarioEvaluationSchema, ScenarioSchema


class ScenarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, owner_id: int, payload: ScenarioSchema) -> ScenarioSchema:
        scenario = Scenario(
            owner_id=owner_id,
            name=payload.name,
            description=payload.description,
            rainfall_delta_pct=payload.rainfall_delta_pct,
            input_cost_delta_pct=payload.input_cost_delta_pct,
            fertilizer_delta_pct=payload.fertilizer_delta_pct,
            cultivar=payload.cultivar,
            bag_price=payload.bag_price,
        )
        self.db.add(scenario)
        await self.db.commit()
        await self.db.refresh(scenario)
        return ScenarioSchema.model_validate(scenario)

    async def evaluate(self, scenario_id: int) -> ScenarioEvaluationSchema:
        scenario = await self.db.get(Scenario, scenario_id)
        projected_yield = max(40.0, 55 * (1 + scenario.rainfall_delta_pct / 100))
        projected_margin = max(1200.0, 1800 * (1 - scenario.input_cost_delta_pct / 100))
        risk = 1 - abs(scenario.rainfall_delta_pct) / 150
        evaluation = ScenarioEvaluation(
            scenario_id=scenario_id,
            projected_yield=projected_yield,
            projected_margin=projected_margin,
            risk_score=round(risk, 2),
            payload={"bag_price": scenario.bag_price, "cultivar": scenario.cultivar},
        )
        self.db.add(evaluation)
        await self.db.commit()
        await self.db.refresh(evaluation)
        return ScenarioEvaluationSchema.model_validate(evaluation)

    async def compare(self, ids: list[int]) -> list[ScenarioEvaluationSchema]:
        stmt = select(ScenarioEvaluation).where(ScenarioEvaluation.scenario_id.in_(ids))
        result = await self.db.execute(stmt)
        evaluations = result.scalars().all()
        return [ScenarioEvaluationSchema.model_validate(e) for e in evaluations]
