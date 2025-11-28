import pytest
from fastapi.testclient import TestClient

from app.api import deps
from app.main import app
from app.schemas import SimulationResult
from app.services import crops as crops_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_db():
    async def _override():
        yield None

    app.dependency_overrides[deps.get_db] = _override
    app.dependency_overrides[deps.rate_limit_dep] = lambda: None
    yield
    app.dependency_overrides.pop(deps.get_db)
    app.dependency_overrides.pop(deps.rate_limit_dep)


def test_simulation(monkeypatch):
    async def fake_run(_self, payload):
        return SimulationResult(
            scenario_name="S1",
            projected_yield=60,
            projected_margin=2000,
            risk_score=0.8,
            breakdown={"bag_price": payload.bag_price},
        )

    monkeypatch.setattr(crops_service.CropService, "run_simulation", fake_run)
    payload = {
        "field_id": 1,
        "rainfall_delta_pct": 10,
        "input_cost_delta_pct": -5,
        "fertilizer_delta_pct": 3,
        "cultivar": "SOJA RR",
        "bag_price": 150,
    }
    response = client.post("/crops/simulation", json=payload)
    assert response.status_code == 200
    assert response.json()["projected_margin"] == 2000
