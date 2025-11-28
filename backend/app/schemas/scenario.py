from datetime import datetime

from pydantic import BaseModel


class ScenarioSchema(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    rainfall_delta_pct: float
    input_cost_delta_pct: float
    fertilizer_delta_pct: float
    cultivar: str
    bag_price: float
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ScenarioEvaluationSchema(BaseModel):
    scenario_id: int
    projected_yield: float
    projected_margin: float
    risk_score: float
    payload: dict | None = None
