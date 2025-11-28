from fastapi import APIRouter

router = APIRouter()


@router.get("/z", summary="Healthcheck básico")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
