from typing import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CropProductivity, CropSimulation, Season
from app.schemas import (
    ProductivitySchema,
    SeasonSchema,
    SimulationCompareRequest,
    SimulationRequest,
    SimulationResult,
)


def _simulate_margin(payload: SimulationRequest, baseline_yield: float, baseline_margin: float) -> SimulationResult:
    rainfall_factor = 1 + payload.rainfall_delta_pct / 100
    input_factor = 1 - payload.input_cost_delta_pct / 100
    fertilizer_factor = 1 + payload.fertilizer_delta_pct / 100
    projected_yield = baseline_yield * rainfall_factor * fertilizer_factor
    projected_margin = baseline_margin * rainfall_factor * input_factor
    risk_score = max(0.1, 1 - (abs(payload.rainfall_delta_pct) + abs(payload.input_cost_delta_pct)) / 200)
    breakdown = {
        "rainfall_effect": rainfall_factor,
        "input_savings": input_factor,
        "fertilizer_effect": fertilizer_factor,
        "bag_price": payload.bag_price,
    }
    return SimulationResult(
        scenario_name=f"{payload.cultivar}-{payload.bag_price}",
        projected_yield=round(projected_yield, 2),
        projected_margin=round(projected_margin, 2),
        risk_score=round(risk_score, 2),
        breakdown=breakdown,
    )


class CropService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_seasons(self) -> list[SeasonSchema]:
        stmt: Select[tuple[Season]] = select(Season).order_by(Season.planting_date.desc())
        seasons = (await self.db.execute(stmt)).scalars().all()
        return [SeasonSchema.model_validate(season) for season in seasons]

    async def list_productivity(self, season_id: int) -> list[ProductivitySchema]:
        stmt = select(CropProductivity).where(CropProductivity.season_id == season_id)
        records: Sequence[CropProductivity] = (await self.db.execute(stmt)).scalars().all()
        return [
            ProductivitySchema(
                season_id=row.season_id,
                area_ha=row.area_ha,
                yield_bag_ha=row.yield_bag_ha,
                ndvi_avg=row.ndvi_avg,
                rainfall_total=row.rainfall_total,
                efficiency_index=row.efficiency_index,
            )
            for row in records
        ]

    async def run_simulation(self, payload: SimulationRequest) -> SimulationResult:
        baseline_stmt = (
            select(func.avg(CropProductivity.yield_bag_ha), func.avg(CropProductivity.efficiency_index))
            .join(Season, Season.id == CropProductivity.season_id)
            .where(Season.field_id == payload.field_id)
        )
        row = (await self.db.execute(baseline_stmt)).one_or_none()
        baseline_yield = float(row[0] or 55)
        baseline_margin = float(row[1] or 1800)
        result = _simulate_margin(payload, baseline_yield, baseline_margin)

        sim = CropSimulation(
            field_id=payload.field_id,
            scenario_name=result.scenario_name,
            delta_rainfall=payload.rainfall_delta_pct,
            delta_inputs=payload.input_cost_delta_pct,
            cultivar=payload.cultivar,
            density_plants_ha=55000,
            expected_margin_per_ha=result.projected_margin,
            payload=result.breakdown,
        )
        self.db.add(sim)
        await self.db.commit()
        return result

    async def compare(self, payload: SimulationCompareRequest) -> list[SimulationResult]:
        results = []
        for scenario in payload.scenarios:
            results.append(await self.run_simulation(scenario))
        return results
