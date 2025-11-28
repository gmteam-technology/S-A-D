from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Enum as PgEnum, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ReportType(str, Enum):
    safra = "safra"
    clima = "clima"
    custos = "custos"
    previsao = "previsao"
    mapas = "mapas"


class ReportJob(Base):
    __tablename__ = "report_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_type: Mapped[ReportType] = mapped_column(PgEnum(ReportType, name="report_type"))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    payload: Mapped[dict | None] = mapped_column(JSON)
    file_url: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
