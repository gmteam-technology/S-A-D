from datetime import date

from pydantic import BaseModel, Field


class SeasonSchema(BaseModel):
    id: int | None = None
    field_id: int
    cultivar: str
    planting_date: date
    harvest_date: date | None = None
    expected_yield_bag_ha: float = Field(gt=0)
    cost_per_ha: float = Field(ge=0)

    class Config:
        from_attributes = True


class ProductivitySchema(BaseModel):
    season_id: int
    area_ha: float
    yield_bag_ha: float
    ndvi_avg: float
    rainfall_total: float
    efficiency_index: float


class SimulationRequest(BaseModel):
    field_id: int
    rainfall_delta_pct: float
    input_cost_delta_pct: float
    fertilizer_delta_pct: float
    cultivar: str
    bag_price: float


class SimulationResult(BaseModel):
    scenario_name: str
    projected_yield: float
    projected_margin: float
    risk_score: float
    breakdown: dict


class SimulationCompareRequest(BaseModel):
    scenarios: list[SimulationRequest]
