from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models import Field, Season, CropProductivity

router = APIRouter()


@router.get("/kpis")
async def get_kpis(
    farm_id: int | None = Query(None),
    field_id: int | None = Query(None),
    variety: str | None = Query(None),
    season: str | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Retorna KPIs agregados baseados nos filtros aplicados.
    """
    # Query base para campos
    query = select(Field)
    
    if farm_id:
        query = query.where(Field.owner_id == farm_id)
    if field_id:
        query = query.where(Field.id == field_id)
    if variety:
        query = query.where(Field.soil_type.contains(variety))  # Ajustar conforme schema real
    
    fields_result = await db.execute(query)
    fields = fields_result.scalars().all()
    
    # Calcular área total
    area_ha = sum(field.area_ha for field in fields) if fields else 0.0
    
    # Query para produtividade
    prod_query = select(
        func.avg(CropProductivity.yield_bag_ha * 60).label("avg_productivity_kg_ha"),  # 1 sc = 60kg
        func.sum(CropProductivity.area_ha * CropProductivity.yield_bag_ha * 60 / 1000).label("total_yield_t")
    ).join(Season).join(Field)
    
    if farm_id:
        prod_query = prod_query.where(Field.owner_id == farm_id)
    if field_id:
        prod_query = prod_query.where(Field.id == field_id)
    if season:
        # Ajustar conforme schema de Season
        pass
    
    prod_result = await db.execute(prod_query)
    prod_row = prod_result.first()
    
    avg_productivity_kg_ha = float(prod_row.avg_productivity_kg_ha) if prod_row.avg_productivity_kg_ha else 0.0
    total_yield_t = float(prod_row.total_yield_t) if prod_row.total_yield_t else 0.0
    
    # Valores mockados para umidade, proteína e margem (implementar queries reais)
    avg_moisture_pct = 13.2
    avg_protein_pct = 38.5
    estimated_margin_r_ha = 2100.0
    
    return {
        "area_ha": round(area_ha, 1),
        "avg_productivity_kg_ha": round(avg_productivity_kg_ha, 1),
        "total_yield_t": round(total_yield_t, 1),
        "avg_moisture_pct": avg_moisture_pct,
        "avg_protein_pct": avg_protein_pct,
        "estimated_margin_r_ha": estimated_margin_r_ha,
        "last_updated": datetime.utcnow().isoformat()
    }


