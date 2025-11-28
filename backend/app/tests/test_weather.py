import pytest
from fastapi.testclient import TestClient

from app.api import deps
from app.main import app
from app.schemas import ForecastResponse, HistoryResponse, StationResponse
from app.services import weather as weather_service

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


def test_list_stations(monkeypatch):
    async def fake_list(_self):
        return [StationResponse(code="BR001", name="Test", latitude=-10.0, longitude=-50.0, elevation=600)]

    monkeypatch.setattr(weather_service.WeatherService, "list_stations", fake_list)
    response = client.get("/weather/stations")
    assert response.status_code == 200
    assert response.json()[0]["code"] == "BR001"


def test_forecast(monkeypatch):
    async def fake_forecast(_self, station):
        return ForecastResponse(station_code=station, generated_at="2025-01-01T00:00:00Z", forecast=[])

    monkeypatch.setattr(weather_service.WeatherService, "get_forecast", fake_forecast)
    response = client.get("/weather/forecast", params={"station": "BR001"})
    assert response.status_code == 200
    assert response.json()["station_code"] == "BR001"


def test_history(monkeypatch):
    async def fake_history(_self, station):
        return HistoryResponse(station_code=station, history=[])

    monkeypatch.setattr(weather_service.WeatherService, "get_history", fake_history)
    response = client.get("/weather/history", params={"station": "BR001"})
    assert response.status_code == 200
    assert response.json()["station_code"] == "BR001"
