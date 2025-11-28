from datetime import datetime

from pydantic import BaseModel

from app.models.report import ReportType


class ReportRequest(BaseModel):
    report_type: ReportType
    params: dict | None = None


class ReportStatus(BaseModel):
    id: int
    report_type: ReportType
    status: str
    file_url: str | None = None
    created_at: datetime
    finished_at: datetime | None = None

    class Config:
        from_attributes = True
