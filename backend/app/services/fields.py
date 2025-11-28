from fastapi import HTTPException, status
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping, shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Field, FieldLayer
from app.schemas import FieldLayerSchema, FieldSchema


class FieldService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_fields(self) -> list[FieldSchema]:
        result = await self.db.execute(select(Field))
        fields = result.scalars().all()
        return [self._to_schema(field) for field in fields]

    async def create(self, payload: FieldSchema, owner_id: int) -> FieldSchema:
        geometry = shape(payload.geometry)
        field = Field(
            name=payload.name,
            area_ha=payload.area_ha,
            soil_type=payload.soil_type,
            drainage_class=payload.drainage_class,
            owner_id=owner_id,
            geometry=f"SRID=4674;{geometry.wkt}",
        )
        self.db.add(field)
        await self.db.commit()
        await self.db.refresh(field)
        return self._to_schema(field)

    async def add_layer(self, field_id: int, payload: FieldLayerSchema) -> FieldLayerSchema:
        field = await self.db.get(Field, field_id)
        if not field:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talhão não encontrado")
        layer = FieldLayer(
            field_id=field_id,
            layer_type=payload.layer_type,
            stats=payload.stats,
            raster_url=payload.raster_url,
        )
        self.db.add(layer)
        await self.db.commit()
        await self.db.refresh(layer)
        return FieldLayerSchema.model_validate(layer)

    def _to_schema(self, field: Field) -> FieldSchema:
        geometry = mapping(to_shape(field.geometry))
        layers = [FieldLayerSchema.model_validate(layer) for layer in field.layers]
        return FieldSchema(
            id=field.id,
            name=field.name,
            area_ha=field.area_ha,
            soil_type=field.soil_type,
            drainage_class=field.drainage_class,
            geometry=geometry,
            layers=layers,
            created_at=field.created_at,
        )
