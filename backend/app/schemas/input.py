from pydantic import BaseModel, Field


class InputItemSchema(BaseModel):
    id: int | None = None
    name: str
    unit: str
    unit_cost: float = Field(gt=0)
    supplier: str | None = None

    class Config:
        from_attributes = True


class CostAnalysisSchema(BaseModel):
    field_id: int
    season_id: int | None = None
    cost_per_ha: float
    margin_expected: float
    delta_price_pct: float
    payload: dict | None = None


class CostComparisonResponse(BaseModel):
    baseline_cost: float
    scenario_cost: float
    sensitivity: dict
