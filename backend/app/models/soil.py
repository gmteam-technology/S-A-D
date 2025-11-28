from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class SoilSample(Base):
    __tablename__ = "soil_samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    depth_cm: Mapped[int]
    ph: Mapped[float]
    organic_matter: Mapped[float]
    nitrogen: Mapped[float]
    phosphorus: Mapped[float]
    potassium: Mapped[float]
    recommendation: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class SoilLayerStat(Base):
    __tablename__ = "soil_layer_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    clay_pct: Mapped[float]
    sand_pct: Mapped[float]
    silt_pct: Mapped[float]
    cec: Mapped[float]
    base_saturation: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
