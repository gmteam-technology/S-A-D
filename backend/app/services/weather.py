from datetime import datetime
from typing import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WeatherForecast, WeatherHistory, WeatherStation
from app.schemas.weather import ForecastResponse, ForecastDay, HistoryResponse, StationResponse, WeatherSummary


class WeatherService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_stations(self) -> list[StationResponse]:
        stmt = select(WeatherStation)
        result = await self.db.execute(stmt)
        stations = result.scalars().all()
        return [
            StationResponse(
                code=s.code,
                name=s.name,
                latitude=s.latitude,
                longitude=s.longitude,
                elevation=s.elevation,
            )
            for s in stations
        ]

    async def get_forecast(self, station_code: str) -> ForecastResponse:
        station_stmt: Select[tuple[WeatherStation]] = select(WeatherStation).where(WeatherStation.code == station_code)
        station = (await self.db.execute(station_stmt)).scalar_one()

        stmt = (
            select(WeatherForecast)
            .where(WeatherForecast.station_id == station.id)
            .order_by(WeatherForecast.forecast_date)
            .limit(10)
        )
        result = await self.db.execute(stmt)
        forecasts: Sequence[WeatherForecast] = result.scalars().all()
        return ForecastResponse(
            station_code=station.code,
            generated_at=datetime.utcnow(),
            forecast=[
                ForecastDay(
                    date=fc.forecast_date,
                    min_temp_c=fc.min_temp_c,
                    max_temp_c=fc.max_temp_c,
                    rainfall_mm=fc.rainfall_mm,
                    risk_index=fc.risk_index,
                )
                for fc in forecasts
            ],
        )

    async def get_history(self, station_code: str) -> HistoryResponse:
        station = (
            await self.db.execute(select(WeatherStation).where(WeatherStation.code == station_code))
        ).scalar_one()
        stmt = (
            select(WeatherHistory)
            .where(WeatherHistory.station_id == station.id)
            .order_by(WeatherHistory.reading_date.desc())
            .limit(30)
        )
        result = await self.db.execute(stmt)
        history = result.scalars().all()
        return HistoryResponse(
            station_code=station.code,
            history=[
                WeatherSummary(
                    station=station.code,
                    rainfall_mm=row.rainfall_mm,
                    temperature_c=row.temperature_c,
                    eto=row.eto,
                    ndvi=row.ndvi,
                )
                for row in history
            ],
        )

    async def get_rainfall_stats(self, station_code: str) -> dict[str, float]:
        station = (
            await self.db.execute(select(WeatherStation).where(WeatherStation.code == station_code))
        ).scalar_one()
        stmt = (
            select(func.avg(WeatherHistory.rainfall_mm), func.sum(WeatherHistory.rainfall_mm))
            .where(WeatherHistory.station_id == station.id)
        )
        result = await self.db.execute(stmt)
        avg_rain, total_rain = result.one()
        return {"avg": float(avg_rain or 0), "total": float(total_rain or 0)}
