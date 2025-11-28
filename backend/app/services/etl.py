import csv
import json
from pathlib import Path

import pandas as pd
from fastapi import UploadFile

from app.schemas import ETLJobResponse, UploadMapping


class ETLService:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def ingest_file(self, file: UploadFile) -> ETLJobResponse:
        target = self.storage_dir / file.filename
        content = await file.read()
        target.write_bytes(content)
        issues: list[str] = []
        if file.filename.endswith(".csv"):
            df = pd.read_csv(target)
            if df.isnull().sum().any():
                issues.append("Valores ausentes detectados")
        elif file.filename.endswith(".xlsx"):
            pd.read_excel(target)
        elif file.filename.endswith(".json"):
            json.loads(target.read_text())
        else:
            issues.append("Formato não suportado, realizar conversão")
        return ETLJobResponse(job_id=file.filename, status="stored", issues=issues)

    def normalize_rainfall(self, csv_path: Path) -> Path:
        df = pd.read_csv(csv_path)
        df["rainfall_mm"] = df["rainfall_mm"].clip(lower=0)
        df["date"] = pd.to_datetime(df["date"])
        out = csv_path.with_name(f"{csv_path.stem}_normalized.csv")
        df.to_csv(out, index=False)
        return out

    def preview_mapping(self, mapping: UploadMapping) -> dict:
        df = pd.read_csv(mapping.file_path, delimiter=mapping.delimiter)
        preview = df.head().rename(columns=mapping.column_map)
        return {"columns": list(preview.columns), "sample": preview.to_dict(orient="records")}
