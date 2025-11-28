import asyncio
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models import ReportJob, ReportType
from app.schemas import ReportRequest, ReportStatus


class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def enqueue(self, payload: ReportRequest) -> ReportStatus:
        job = ReportJob(report_type=payload.report_type, payload=payload.params)
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        asyncio.create_task(self._render_pdf(job.id, payload))
        return ReportStatus.model_validate(job)

    async def _render_pdf(self, job_id: int, payload: ReportRequest) -> None:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        c.drawString(72, 800, f"Relatório {payload.report_type.value.upper()}")
        c.drawString(72, 780, f"Gerado em: {datetime.utcnow().isoformat()}Z")
        if payload.params:
            y = 760
            for key, value in payload.params.items():
                c.drawString(72, y, f"{key}: {value}")
                y -= 16
        c.showPage()
        c.save()
        buf.seek(0)
        async with get_session() as session:
            job = await session.get(ReportJob, job_id)
            job.status = "finished"
            job.file_url = f"s3://siad-reports/{job_id}.pdf"
            job.finished_at = datetime.utcnow()
            await session.commit()

    async def list_jobs(self) -> list[ReportStatus]:
        result = await self.db.execute(select(ReportJob).order_by(ReportJob.created_at.desc()))
        jobs = result.scalars().all()
        return [ReportStatus.model_validate(job) for job in jobs]
