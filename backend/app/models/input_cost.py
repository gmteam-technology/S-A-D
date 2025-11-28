from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class InputItem(Base):
    __tablename__ = "input_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    unit: Mapped[str] = mapped_column(String(16))
    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2))
    supplier: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class InputCostAnalysis(Base):
    __tablename__ = "input_cost_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    season_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("seasons.id", ondelete="SET NULL"))
    cost_per_ha: Mapped[float] = mapped_column(Numeric(12, 2))
    margin_expected: Mapped[float] = mapped_column(Numeric(12, 2))
    delta_price_pct: Mapped[float]
    payload: Mapped[dict | None]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
