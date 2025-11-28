from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from app.core.config import get_settings
from app.schemas import ETLJobResponse, UploadMapping
from app.services.etl import ETLService

router = APIRouter()
settings = get_settings()
storage_dir = Path(settings.storage_dir)
etl_service = ETLService(storage_dir)


@router.post("/upload", response_model=ETLJobResponse)
async def upload(file: UploadFile = File(...)) -> ETLJobResponse:
    return await etl_service.ingest_file(file)


@router.post("/normalize/rainfall")
async def normalize_rainfall(file_path: str) -> dict[str, str]:
    out = etl_service.normalize_rainfall(Path(file_path))
    return {"normalized_file": str(out)}


@router.post("/preview")
async def preview(mapping: UploadMapping) -> dict:
    return etl_service.preview_mapping(mapping)
