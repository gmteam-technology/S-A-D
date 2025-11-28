from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas import ReportRequest, ReportStatus
from app.services.reports import ReportService

router = APIRouter()


@router.post("", response_model=ReportStatus)
async def create_report(payload: ReportRequest, db: AsyncSession = Depends(get_db)) -> ReportStatus:
    return await ReportService(db).enqueue(payload)


@router.get("", response_model=list[ReportStatus])
async def list_reports(db: AsyncSession = Depends(get_db)) -> list[ReportStatus]:
    return await ReportService(db).list_jobs()
