from __future__ import annotations

import asyncio
from pathlib import Path

import typer

from app.services.etl import ETLService

app = typer.Typer(help="CLI para pipelines ETL")


@app.command()
def run(file_path: Path) -> None:
    service = ETLService(Path("/workspace/storage/uploads"))
    result = asyncio.run(service.ingest_file(_build_upload(file_path)))
    typer.echo(result.model_dump())


def _build_upload(file_path: Path):
    from fastapi import UploadFile

    return UploadFile(filename=file_path.name, file=open(file_path, "rb"))


if __name__ == "__main__":
    app()
