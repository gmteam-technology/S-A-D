from pydantic import BaseModel, Field


class SoilSampleSchema(BaseModel):
    field_id: int
    depth_cm: int = Field(gt=0)
    ph: float
    organic_matter: float
    nitrogen: float
    phosphorus: float
    potassium: float
    recommendation: str | None = None


class SoilAnalysisResponse(BaseModel):
    field_id: int
    lime_recommendation_kg_ha: float
    fertilizer_plan: dict
    warnings: list[str]
