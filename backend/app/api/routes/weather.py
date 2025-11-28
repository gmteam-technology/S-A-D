from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas import ForecastResponse, HistoryResponse, StationResponse
from app.services.weather import WeatherService

router = APIRouter()


@router.get("/stations", response_model=list[StationResponse])
async def stations(db: AsyncSession = Depends(get_db)) -> list[StationResponse]:
    service = WeatherService(db)
    return await service.list_stations()


@router.get("/forecast", response_model=ForecastResponse)
async def forecast(station: str, db: AsyncSession = Depends(get_db)) -> ForecastResponse:
    service = WeatherService(db)
    try:
        return await service.get_forecast(station)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/history", response_model=HistoryResponse)
async def history(station: str, db: AsyncSession = Depends(get_db)) -> HistoryResponse:
    service = WeatherService(db)
    return await service.get_history(station)
