from fastapi import APIRouter, Depends

from app.api import deps

from . import auth, weather, crops, scenarios, soil, fields, inputs, reports, etl, health, dashboard, prices

api_router = APIRouter(dependencies=[Depends(deps.rate_limit_dep)])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
api_router.include_router(soil.router, prefix="/soil", tags=["soil"])
api_router.include_router(fields.router, prefix="/fields", tags=["fields"])
api_router.include_router(inputs.router, prefix="/inputs", tags=["inputs"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(etl.router, prefix="/etl", tags=["etl"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(prices.router, prefix="/prices", tags=["prices"])
