from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery(
    "siad",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


@celery_app.task
def run_monte_carlo(payload: dict) -> dict:
    import random

    iterations = payload.get("iterations", 1000)
    bag_price = payload.get("bag_price", 150)
    rainfall_pct = payload.get("rainfall_delta_pct", 0)
    input_pct = payload.get("input_cost_delta_pct", 0)
    results = []
    for _ in range(iterations):
        rainfall = 1 + random.gauss(rainfall_pct / 100, 0.05)
        inputs = 1 - random.gauss(input_pct / 100, 0.05)
        yield_base = random.uniform(45, 65)
        margin_base = random.uniform(1400, 2200)
        results.append({
            "yield": yield_base * rainfall,
            "margin": margin_base * rainfall * inputs,
        })
    avg_yield = sum(r["yield"] for r in results) / iterations
    avg_margin = sum(r["margin"] for r in results) / iterations
    return {"yield": round(avg_yield, 2), "margin": round(avg_margin, 2), "bag_price": bag_price}
