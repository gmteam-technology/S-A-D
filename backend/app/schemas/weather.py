from datetime import date, datetime

from pydantic import BaseModel


class WeatherSummary(BaseModel):
    station: str
    rainfall_mm: float
    temperature_c: float
    eto: float
    ndvi: float


class ForecastDay(BaseModel):
    date: date
    min_temp_c: float
    max_temp_c: float
    rainfall_mm: float
    risk_index: float


class ForecastResponse(BaseModel):
    station_code: str
    generated_at: datetime
    forecast: list[ForecastDay]


class HistoryResponse(BaseModel):
    station_code: str
    history: list[WeatherSummary]


class StationResponse(BaseModel):
    code: str
    name: str
    latitude: float
    longitude: float
    elevation: float | None
