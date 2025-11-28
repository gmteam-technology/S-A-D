from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field as PydanticField


class FieldLayerSchema(BaseModel):
    id: int | None = None
    layer_type: Literal["solo", "drenagem", "ndvi", "clima", "produtividade"]
    stats: dict | None = None
    raster_url: str | None = None

    class Config:
        from_attributes = True


class FieldSchema(BaseModel):
    id: int | None = None
    name: str
    area_ha: float = PydanticField(gt=0)
    soil_type: str | None = None
    drainage_class: str | None = None
    geometry: dict
    layers: list[FieldLayerSchema] = PydanticField(default_factory=list)
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class FieldLayerCreate(BaseModel):
    layer_type: Literal["solo", "drenagem", "ndvi", "clima", "produtividade"]
    stats: dict | None = None
    raster_url: str | None = None
