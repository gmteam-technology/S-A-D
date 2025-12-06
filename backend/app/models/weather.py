from datetime import date, datetime

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class WeatherStation(Base):
    __tablename__ = "weather_stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    elevation: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("weather_stations.id", ondelete="CASCADE"))
    reading_date: Mapped[date]
    rainfall_mm: Mapped[float]
    temperature_c: Mapped[float]
    eto: Mapped[float]
    ndvi: Mapped[float]


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("weather_stations.id", ondelete="CASCADE"))
    forecast_date: Mapped[date]
    min_temp_c: Mapped[float]
    max_temp_c: Mapped[float]
    rainfall_mm: Mapped[float]
    risk_index: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class RadarSnapshot(Base):
    __tablename__ = "radar_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    geojson_url: Mapped[str] = mapped_column(String(512))
    metadata_json: Mapped[dict | None] = mapped_column("metadata")


class ClimaticIndicator(Base):
    __tablename__ = "climatic_indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    kc: Mapped[float]
    eto: Mapped[float]
    ndvi: Mapped[float]
    rainfall_anomaly: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
