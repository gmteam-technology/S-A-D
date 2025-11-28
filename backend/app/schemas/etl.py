from pathlib import Path

from pydantic import BaseModel, FilePath


class ETLJobResponse(BaseModel):
    job_id: str
    status: str
    issues: list[str] = []


class UploadMapping(BaseModel):
    file_path: FilePath
    delimiter: str = ","
    column_map: dict[str, str]


class GeoValidationResult(BaseModel):
    features: int
    invalid_features: int
    suggested_fixes: list[str]
