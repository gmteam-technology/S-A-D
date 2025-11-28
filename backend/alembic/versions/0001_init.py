"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2025-11-28
"""

from alembic import op
import sqlalchemy as sa
import geoalchemy2


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    user_role = sa.Enum("produtor", "agronomo", "gestor", "visualizador", name="user_role")
    report_type = sa.Enum("safra", "clima", "custos", "previsao", "mapas", name="report_type")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("locale", sa.String(8), nullable=False, server_default="pt-BR"),
        sa.Column("preferences", sa.JSON, server_default=sa.text("'{}'::jsonb")),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("payload", sa.JSON),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("token", sa.Text, nullable=False, unique=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("revoked", sa.Boolean, server_default=sa.text("false")),
    )

    op.create_table(
        "fields",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("area_ha", sa.Float, nullable=False),
        sa.Column("geometry", geoalchemy2.types.Geometry(geometry_type="MULTIPOLYGON", srid=4674)),
        sa.Column("soil_type", sa.String(64)),
        sa.Column("drainage_class", sa.String(64)),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("metadata", sa.JSON, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "weather_stations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(32), unique=True),
        sa.Column("name", sa.String(128)),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("elevation", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "weather_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("station_id", sa.Integer, sa.ForeignKey("weather_stations.id", ondelete="CASCADE")),
        sa.Column("reading_date", sa.Date, nullable=False),
        sa.Column("rainfall_mm", sa.Float, nullable=False),
        sa.Column("temperature_c", sa.Float, nullable=False),
        sa.Column("eto", sa.Float, nullable=False),
        sa.Column("ndvi", sa.Float, nullable=False),
    )

    op.create_table(
        "weather_forecasts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("station_id", sa.Integer, sa.ForeignKey("weather_stations.id", ondelete="CASCADE")),
        sa.Column("forecast_date", sa.Date, nullable=False),
        sa.Column("min_temp_c", sa.Float, nullable=False),
        sa.Column("max_temp_c", sa.Float, nullable=False),
        sa.Column("rainfall_mm", sa.Float, nullable=False),
        sa.Column("risk_index", sa.Float, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "radar_snapshots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("geojson_url", sa.String(512)),
        sa.Column("metadata", sa.JSON),
    )

    op.create_table(
        "climatic_indicators",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("kc", sa.Float),
        sa.Column("eto", sa.Float),
        sa.Column("ndvi", sa.Float),
        sa.Column("rainfall_anomaly", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "field_layers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("layer_type", sa.String(32), nullable=False),
        sa.Column("source", sa.String(128)),
        sa.Column("stats", sa.JSON),
        sa.Column("raster_url", sa.String(512)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "field_sensors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("sensor_type", sa.String(64)),
        sa.Column("unit", sa.String(32)),
        sa.Column("last_value", sa.Numeric(10, 2)),
        sa.Column("metadata", sa.JSON),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("cultivar", sa.String(64), nullable=False),
        sa.Column("planting_date", sa.Date, nullable=False),
        sa.Column("harvest_date", sa.Date),
        sa.Column("expected_yield_bag_ha", sa.Float, nullable=False),
        sa.Column("cost_per_ha", sa.Float, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "crop_productivity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("season_id", sa.Integer, sa.ForeignKey("seasons.id", ondelete="CASCADE")),
        sa.Column("area_ha", sa.Float),
        sa.Column("yield_bag_ha", sa.Float),
        sa.Column("ndvi_avg", sa.Float),
        sa.Column("rainfall_total", sa.Float),
        sa.Column("efficiency_index", sa.Float),
    )

    op.create_table(
        "crop_simulations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("scenario_name", sa.String(128)),
        sa.Column("delta_rainfall", sa.Float),
        sa.Column("delta_inputs", sa.Float),
        sa.Column("cultivar", sa.String(64)),
        sa.Column("density_plants_ha", sa.Integer),
        sa.Column("expected_margin_per_ha", sa.Float),
        sa.Column("payload", sa.JSON),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("name", sa.String(128)),
        sa.Column("description", sa.String(512)),
        sa.Column("rainfall_delta_pct", sa.Float),
        sa.Column("input_cost_delta_pct", sa.Float),
        sa.Column("fertilizer_delta_pct", sa.Float),
        sa.Column("cultivar", sa.String(64)),
        sa.Column("bag_price", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "scenario_evaluations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("scenario_id", sa.Integer, sa.ForeignKey("scenarios.id", ondelete="CASCADE")),
        sa.Column("projected_yield", sa.Float),
        sa.Column("projected_margin", sa.Float),
        sa.Column("risk_score", sa.Float),
        sa.Column("payload", sa.JSON),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "soil_samples",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("depth_cm", sa.Integer),
        sa.Column("ph", sa.Float),
        sa.Column("organic_matter", sa.Float),
        sa.Column("nitrogen", sa.Float),
        sa.Column("phosphorus", sa.Float),
        sa.Column("potassium", sa.Float),
        sa.Column("recommendation", sa.String(512)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "soil_layer_stats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("clay_pct", sa.Float),
        sa.Column("sand_pct", sa.Float),
        sa.Column("silt_pct", sa.Float),
        sa.Column("cec", sa.Float),
        sa.Column("base_saturation", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "input_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(128)),
        sa.Column("unit", sa.String(16)),
        sa.Column("unit_cost", sa.Numeric(12, 2)),
        sa.Column("supplier", sa.String(128)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "input_cost_analysis",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("field_id", sa.Integer, sa.ForeignKey("fields.id", ondelete="CASCADE")),
        sa.Column("season_id", sa.Integer, sa.ForeignKey("seasons.id", ondelete="SET NULL")),
        sa.Column("cost_per_ha", sa.Numeric(12, 2)),
        sa.Column("margin_expected", sa.Numeric(12, 2)),
        sa.Column("delta_price_pct", sa.Float),
        sa.Column("payload", sa.JSON),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "report_jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("report_type", report_type, nullable=False),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("payload", sa.JSON),
        sa.Column("file_url", sa.String(512)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.Column("finished_at", sa.TIMESTAMP(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("report_jobs")
    op.drop_table("input_cost_analysis")
    op.drop_table("input_items")
    op.drop_table("soil_layer_stats")
    op.drop_table("soil_samples")
    op.drop_table("scenario_evaluations")
    op.drop_table("scenarios")
    op.drop_table("crop_simulations")
    op.drop_table("crop_productivity")
    op.drop_table("seasons")
    op.drop_table("field_sensors")
    op.drop_table("field_layers")
    op.drop_table("climatic_indicators")
    op.drop_table("radar_snapshots")
    op.drop_table("weather_forecasts")
    op.drop_table("weather_history")
    op.drop_table("weather_stations")
    op.drop_table("fields")
    op.drop_table("refresh_tokens")
    op.drop_table("audit_logs")
    op.drop_table("users")
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="report_type").drop(op.get_bind(), checkfirst=False)
