"""Scripts de seed contendo mais de 200 linhas com dados agrícolas."""
from __future__ import annotations

import asyncio
from datetime import date, timedelta
from random import randint, uniform

import typer
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db.session import Base
from app.models import (
    Field,
    FieldLayer,
    InputItem,
    Scenario,
    Season,
    SoilSample,
    User,
    UserRole,
    WeatherForecast,
    WeatherHistory,
    WeatherStation,
)

app = typer.Typer(help="Seeds para o SIAD Agro")
settings = get_settings()


WEATHER_DATA = [
    {"code": "BR001", "name": "Sorriso", "lat": -12.54, "lon": -55.72, "elev": 365},
    {"code": "BR002", "name": "Rondonópolis", "lat": -16.47, "lon": -54.62, "elev": 284},
    {"code": "BR003", "name": "Rio Verde", "lat": -17.78, "lon": -50.90, "elev": 748},
    {"code": "BR004", "name": "Cascavel", "lat": -24.95, "lon": -53.45, "elev": 781},
    {"code": "BR005", "name": "Londrina", "lat": -23.30, "lon": -51.16, "elev": 610},
    {"code": "BR006", "name": "Uberlândia", "lat": -18.91, "lon": -48.27, "elev": 863},
    {"code": "BR007", "name": "Chapecó", "lat": -27.10, "lon": -52.61, "elev": 679},
    {"code": "BR008", "name": "Passo Fundo", "lat": -28.26, "lon": -52.40, "elev": 687},
    {"code": "BR009", "name": "Luziânia", "lat": -16.25, "lon": -47.95, "elev": 930},
    {"code": "BR010", "name": "Primavera do Leste", "lat": -15.55, "lon": -54.28, "elev": 636},
    {"code": "BR011", "name": "Paragominas", "lat": -2.96, "lon": -47.49, "elev": 89},
    {"code": "BR012", "name": "Barreiras", "lat": -12.15, "lon": -45.00, "elev": 452},
    {"code": "BR013", "name": "Balsas", "lat": -7.53, "lon": -46.03, "elev": 277},
    {"code": "BR014", "name": "Gurupi", "lat": -11.72, "lon": -49.06, "elev": 287},
    {"code": "BR015", "name": "Irecê", "lat": -11.30, "lon": -41.86, "elev": 750},
    {"code": "BR016", "name": "Juína", "lat": -11.37, "lon": -58.74, "elev": 377},
    {"code": "BR017", "name": "Campo Novo", "lat": -13.69, "lon": -57.89, "elev": 469},
    {"code": "BR018", "name": "Alta Floresta", "lat": -9.87, "lon": -56.08, "elev": 283},
    {"code": "BR019", "name": "Maracaju", "lat": -21.61, "lon": -55.17, "elev": 384},
    {"code": "BR020", "name": "Dourados", "lat": -22.22, "lon": -54.81, "elev": 430},
    {"code": "BR021", "name": "Sinop", "lat": -11.86, "lon": -55.50, "elev": 371},
    {"code": "BR022", "name": "Querência", "lat": -12.60, "lon": -52.20, "elev": 368},
    {"code": "BR023", "name": "Canarana", "lat": -13.55, "lon": -52.27, "elev": 411},
    {"code": "BR024", "name": "Lucas do Rio Verde", "lat": -13.06, "lon": -55.91, "elev": 398},
    {"code": "BR025", "name": "Formosa", "lat": -15.54, "lon": -47.33, "elev": 912},
    {"code": "BR026", "name": "Bebedouro", "lat": -20.95, "lon": -48.50, "elev": 573},
    {"code": "BR027", "name": "Catalão", "lat": -18.17, "lon": -47.95, "elev": 840},
    {"code": "BR028", "name": "Unaí", "lat": -16.36, "lon": -46.89, "elev": 588},
    {"code": "BR029", "name": "Patos de Minas", "lat": -18.58, "lon": -46.52, "elev": 815},
    {"code": "BR030", "name": "Ituiutaba", "lat": -18.97, "lon": -49.46, "elev": 544},
]

INPUT_CATALOG = [
    ("Semente Soja RR", "saca", 145.0, "AgroSeed"),
    ("Uréia", "kg", 2.8, "FertAgro"),
    ("MAP", "kg", 3.6, "FertAgro"),
    ("KCl", "kg", 3.2, "Nutrimax"),
    ("Glifosato WG", "L", 42.0, "DefenCrop"),
    ("Inseticida Lambda", "L", 65.0, "Protec"),
    ("Fungicida Triazol", "L", 88.0, "Protec"),
    ("Adjuvante Óleo", "L", 22.0, "AgroOil"),
]


async def seed_weather(session: AsyncSession) -> None:
    stations = [WeatherStation(code=row["code"], name=row["name"], latitude=row["lat"], longitude=row["lon"], elevation=row["elev"]) for row in WEATHER_DATA]
    session.add_all(stations)
    await session.flush()
    today = date.today()
    for station in stations:
        for days in range(0, 30):
            reading_date = today - timedelta(days=days)
            session.add(
                WeatherHistory(
                    station_id=station.id,
                    reading_date=reading_date,
                    rainfall_mm=round(uniform(0, 25), 2),
                    temperature_c=round(uniform(18, 34), 1),
                    eto=round(uniform(3.5, 5.5), 2),
                    ndvi=round(uniform(0.45, 0.82), 2),
                )
            )
        for days in range(1, 8):
            forecast_date = today + timedelta(days=days)
            session.add(
                WeatherForecast(
                    station_id=station.id,
                    forecast_date=forecast_date,
                    min_temp_c=round(uniform(18, 22), 1),
                    max_temp_c=round(uniform(30, 36), 1),
                    rainfall_mm=round(uniform(0, 20), 2),
                    risk_index=round(uniform(0.1, 0.9), 2),
                )
            )


async def seed_users(session: AsyncSession) -> list[User]:
    await session.execute(delete(User))
    admin = User(
        email="gestor@siad.ag",
        full_name="Gestor Master",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.gestor,
    )
    agronomist = User(
        email="agronomo@siad.ag",
        full_name="Eng. Agrônomo",
        hashed_password=get_password_hash("agro123"),
        role=UserRole.agronomo,
    )
    producer = User(
        email="produtor@siad.ag",
        full_name="Produtor Rural",
        hashed_password=get_password_hash("campo123"),
        role=UserRole.produtor,
    )
    viewer = User(
        email="viewer@siad.ag",
        full_name="Analista",
        hashed_password=get_password_hash("viewer123"),
        role=UserRole.visualizador,
    )
    session.add_all([admin, agronomist, producer, viewer])
    await session.flush()
    return [admin, agronomist, producer, viewer]


async def seed_fields(session: AsyncSession, owner_id: int) -> list[Field]:
    polygons = [
        "POLYGON((-55.95 -12.55,-55.94 -12.55,-55.94 -12.54,-55.95 -12.54,-55.95 -12.55))",
        "POLYGON((-54.70 -16.48,-54.69 -16.48,-54.69 -16.47,-54.70 -16.47,-54.70 -16.48))",
        "POLYGON((-50.91 -17.79,-50.90 -17.79,-50.90 -17.78,-50.91 -17.78,-50.91 -17.79))",
        "POLYGON((-53.46 -24.96,-53.45 -24.96,-53.45 -24.95,-53.46 -24.95,-53.46 -24.96))",
        "POLYGON((-51.17 -23.31,-51.16 -23.31,-51.16 -23.30,-51.17 -23.30,-51.17 -23.31))",
    ]
    fields: list[Field] = []
    for idx, wkt in enumerate(polygons, start=1):
        field = Field(
            name=f"Talhão {idx}",
            area_ha=round(uniform(45, 120), 2),
            geometry=f"SRID=4674;{wkt}",
            soil_type="Latossolo Vermelho",
            drainage_class="Boa",
            owner_id=owner_id,
        )
        session.add(field)
        fields.append(field)
    await session.flush()
    for field in fields:
        session.add(
            FieldLayer(
                field_id=field.id,
                layer_type="ndvi",
                stats={"avg": round(uniform(0.55, 0.75), 2)},
                raster_url=f"s3://siad/ndvi/{field.id}.tif",
            )
        )
    return fields


async def seed_seasons(session: AsyncSession, field: Field) -> None:
    plant_date = date(2024, 10, 15)
    harvest_date = date(2025, 2, 20)
    season = Season(
        field_id=field.id,
        cultivar="SOJA RR",
        planting_date=plant_date,
        harvest_date=harvest_date,
        expected_yield_bag_ha=60,
        cost_per_ha=4200,
    )
    session.add(season)
    await session.flush()
    for idx in range(1, 6):
        await session.execute(
            WeatherHistory.__table__.insert(),
            {
                "station_id": 1,
                "reading_date": plant_date + timedelta(days=idx * 10),
                "rainfall_mm": 15 + idx,
                "temperature_c": 28 + idx * 0.3,
                "eto": 4.2,
                "ndvi": 0.55 + idx * 0.03,
            },
        )


async def seed_soil_samples(session: AsyncSession, field: Field) -> None:
    depths = [0, 10, 20, 40, 60]
    for depth in depths:
        session.add(
            SoilSample(
                field_id=field.id,
                depth_cm=depth,
                ph=round(5.5 + depth * 0.01, 2),
                organic_matter=round(2.5 + depth * 0.02, 2),
                nitrogen=round(18 - depth * 0.1, 2),
                phosphorus=round(14 - depth * 0.08, 2),
                potassium=round(210 - depth * 0.9, 2),
                recommendation="Aplicar 1,5 t/ha de calcário",
            )
        )


async def seed_inputs(session: AsyncSession) -> None:
    for name, unit, cost, supplier in INPUT_CATALOG:
        session.add(InputItem(name=name, unit=unit, unit_cost=cost, supplier=supplier))


async def seed_scenarios(session: AsyncSession, owner_id: int) -> None:
    for delta in [-10, 0, 10]:
        session.add(
            Scenario(
                owner_id=owner_id,
                name=f"Cenário {delta:+}",
                description="Simulação automática",
                rainfall_delta_pct=delta,
                input_cost_delta_pct=delta / 2,
                fertilizer_delta_pct=delta / 3,
                cultivar="SOJA RR",
                bag_price=155 + delta,
            )
        )


async def seed_all(dataset: str) -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        await seed_weather(session)
        users = await seed_users(session)
        fields = await seed_fields(session, users[0].id)
        for field in fields:
            await seed_seasons(session, field)
            await seed_soil_samples(session, field)
        await seed_inputs(session)
        await seed_scenarios(session, users[0].id)
        await session.commit()
    typer.echo(f"Seeds aplicados: {dataset}")


@app.command()
def run(dataset: str = typer.Argument("base", help="Identificador do dataset")) -> None:
    """Executa a carga de seeds."""
    asyncio.run(seed_all(dataset))


if __name__ == "__main__":
    app()
