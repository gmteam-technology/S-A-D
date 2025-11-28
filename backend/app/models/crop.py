from datetime import date, datetime

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    cultivar: Mapped[str] = mapped_column(String(64))
    planting_date: Mapped[date]
    harvest_date: Mapped[date | None]
    expected_yield_bag_ha: Mapped[float]
    cost_per_ha: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class CropProductivity(Base):
    __tablename__ = "crop_productivity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(Integer, ForeignKey("seasons.id", ondelete="CASCADE"))
    area_ha: Mapped[float]
    yield_bag_ha: Mapped[float]
    ndvi_avg: Mapped[float]
    rainfall_total: Mapped[float]
    efficiency_index: Mapped[float]


class CropSimulation(Base):
    __tablename__ = "crop_simulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    scenario_name: Mapped[str] = mapped_column(String(128))
    delta_rainfall: Mapped[float]
    delta_inputs: Mapped[float]
    cultivar: Mapped[str]
    density_plants_ha: Mapped[int]
    expected_margin_per_ha: Mapped[float]
    payload: Mapped[dict | None]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    season: Mapped[Season] = relationship(lazy="joined")
