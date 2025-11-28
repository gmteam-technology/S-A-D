from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(String(512))
    rainfall_delta_pct: Mapped[float]
    input_cost_delta_pct: Mapped[float]
    fertilizer_delta_pct: Mapped[float]
    cultivar: Mapped[str]
    bag_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)


class ScenarioEvaluation(Base):
    __tablename__ = "scenario_evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(Integer, ForeignKey("scenarios.id", ondelete="CASCADE"))
    projected_yield: Mapped[float]
    projected_margin: Mapped[float]
    risk_score: Mapped[float]
    payload: Mapped[dict | None]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
