from datetime import datetime
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import JSON, Float, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class LayerType(str, Enum):
    solo = "solo"
    drenagem = "drenagem"
    ndvi = "ndvi"
    clima = "clima"
    produtividade = "produtividade"


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    area_ha: Mapped[float] = mapped_column(Float, nullable=False)
    geometry: Mapped[str] = mapped_column(Geometry("MULTIPOLYGON", srid=4674))
    soil_type: Mapped[str | None] = mapped_column(String(64))
    drainage_class: Mapped[str | None] = mapped_column(String(64))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    field_metadata: Mapped[dict | None] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    layers: Mapped[list["FieldLayer"]] = relationship(back_populates="field", cascade="all, delete-orphan")


class FieldLayer(Base):
    __tablename__ = "field_layers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    layer_type: Mapped[LayerType] = mapped_column(String(32), nullable=False)
    source: Mapped[str | None] = mapped_column(String(128))
    stats: Mapped[dict | None] = mapped_column(JSON)
    raster_url: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    field: Mapped[Field] = relationship(back_populates="layers")


class FieldSensor(Base):
    __tablename__ = "field_sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    sensor_type: Mapped[str] = mapped_column(String(64))
    unit: Mapped[str] = mapped_column(String(32))
    last_value: Mapped[float | None] = mapped_column(Numeric(10, 2))
    sensor_metadata: Mapped[dict | None] = mapped_column("metadata", JSON)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
