from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User
from app.schemas import FieldLayerSchema, FieldSchema
from app.services.fields import FieldService

router = APIRouter()


@router.get("", response_model=list[FieldSchema])
async def list_fields(db: AsyncSession = Depends(deps.get_db)) -> list[FieldSchema]:
    return await FieldService(db).list_fields()


@router.post("", response_model=FieldSchema)
async def create_field(
    payload: FieldSchema,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> FieldSchema:
    return await FieldService(db).create(payload, current_user.id)


@router.post("/{field_id}/layers", response_model=FieldLayerSchema)
async def add_layer(field_id: int, payload: FieldLayerSchema, db: AsyncSession = Depends(deps.get_db)) -> FieldLayerSchema:
    return await FieldService(db).add_layer(field_id, payload)
