# Especificação de APIs - Sistema de Gestão de Safra

## Base URL
```
https://api.siad-agro.com/v1
```

## Autenticação
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 1. Dashboard & KPIs

### GET /dashboard/kpis
Retorna KPIs agregados baseados nos filtros aplicados.

**Query Parameters:**
```json
{
  "farm_id": "integer (optional)",
  "field_id": "integer (optional)",
  "variety": "string (optional)",
  "season": "string (optional)",
  "date_from": "ISO8601 (optional)",
  "date_to": "ISO8601 (optional)"
}
```

**Response 200:**
```json
{
  "area_ha": 1250.5,
  "avg_productivity_kg_ha": 3450.2,
  "total_yield_t": 4312.8,
  "avg_moisture_pct": 13.2,
  "avg_protein_pct": 38.5,
  "estimated_margin_r_ha": 2100.0,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

---

## 2. Mapa Agro

### GET /map/fields
Retorna geometrias dos talhões (GeoJSON).

**Query Parameters:**
```json
{
  "farm_id": "integer (optional)",
  "bbox": "min_lon,min_lat,max_lon,max_lat (optional)"
}
```

**Response 200:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-55.95, -12.55], [-55.94, -12.55], ...]]
      },
      "properties": {
        "field_id": 1,
        "name": "Talhão 1",
        "area_ha": 45.2,
        "variety": "BMX Potência RR",
        "planting_date": "2024-10-20",
        "harvest_date": "2025-02-15",
        "yield_kg_ha": 3450.0
      }
    }
  ]
}
```

### GET /map/ndvi/{field_id}
Retorna dados NDVI para um talhão (timeseries ou raster).

**Query Parameters:**
```json
{
  "date": "YYYY-MM-DD (optional)",
  "format": "timeseries | raster (default: timeseries)"
}
```

**Response 200 (timeseries):**
```json
{
  "field_id": 1,
  "data": [
    {
      "date": "2024-10-20",
      "ndvi_mean": 0.72,
      "ndvi_min": 0.65,
      "ndvi_max": 0.78,
      "cloud_coverage_pct": 5.2,
      "source": "Sentinel-2"
    }
  ]
}
```

**Response 200 (raster):**
```
Content-Type: image/tiff
[GeoTIFF binary data]
```

### GET /map/soil/{field_id}
Retorna dados de solo (pontos de amostragem + interpolação).

**Response 200:**
```json
{
  "field_id": 1,
  "samples": [
    {
      "id": 1,
      "coordinates": [-55.95, -12.55],
      "ph": 6.2,
      "organic_matter_pct": 3.5,
      "p_mg_dm3": 12.3,
      "k_cmol_dm3": 0.85,
      "sampling_date": "2024-09-15"
    }
  ],
  "interpolation": {
    "type": "kriging",
    "raster_url": "/api/map/soil/1/raster",
    "uncertainty_url": "/api/map/soil/1/uncertainty"
  }
}
```

### GET /map/climate/{field_id}
Retorna dados climáticos (raster ou timeline).

**Query Parameters:**
```json
{
  "date": "YYYY-MM-DD (optional)",
  "variable": "precipitation | temperature | eto (default: precipitation)"
}
```

**Response 200:**
```json
{
  "field_id": 1,
  "date": "2024-01-15",
  "precipitation_mm": 12.5,
  "temperature_min_c": 18.5,
  "temperature_max_c": 28.3,
  "eto_mm": 4.2,
  "source": "INMET",
  "raster_url": "/api/map/climate/1/raster?date=2024-01-15"
}
```

### GET /map/productivity/{field_id}
Retorna heatmap de produtividade.

**Response 200:**
```json
{
  "field_id": 1,
  "raster_url": "/api/map/productivity/1/raster",
  "statistics": {
    "mean_kg_ha": 3450.2,
    "min_kg_ha": 2800.0,
    "max_kg_ha": 4100.0,
    "std_dev": 250.5
  }
}
```

### GET /map/infrastructure
Retorna infraestrutura (estradas, armazéns, silos).

**Response 200:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[-55.95, -12.55], [-55.94, -12.55]]
      },
      "properties": {
        "type": "road",
        "name": "Estrada Principal",
        "surface": "asphalt"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-55.95, -12.55]
      },
      "properties": {
        "type": "silo",
        "name": "Silo Central",
        "capacity_t": 5000.0
      }
    }
  ]
}
```

### GET /map/alerts/{field_id}
Retorna alertas fitossanitários.

**Response 200:**
```json
{
  "field_id": 1,
  "alerts": [
    {
      "id": 1,
      "type": "disease",
      "severity": "high",
      "disease": "Ferrugem Asiática",
      "coordinates": [-55.95, -12.55],
      "detected_date": "2024-01-10",
      "recommendation": "Aplicar fungicida triazol + estrobilurina"
    }
  ]
}
```

---

## 3. Preços (Atualização a cada 5 minutos)

### GET /prices/current
Retorna preços atuais (com cache de 5 minutos).

**Query Parameters:**
```json
{
  "commodity": "soybean | fertilizer | freight (optional, default: all)"
}
```

**Response 200:**
```json
{
  "soybean": {
    "spot": {
      "price_r_sc": 185.50,
      "price_r_t": 3108.33,
      "source": "CEPEA/ESALQ",
      "timestamp": "2024-01-15T10:30:00Z",
      "last_updated": "2024-01-15T10:25:00Z",
      "cache_ttl_seconds": 300
    },
    "contract": {
      "price_r_sc": 188.20,
      "maturity": "2025-03",
      "source": "B3",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  },
  "fertilizer": {
    "npk_10_10_10": {
      "price_r_t": 3450.00,
      "source": "ANDA",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  },
  "freight": {
    "price_r_t": 85.00,
    "route": "Fazenda → Port",
    "distance_km": 120,
    "source": "AgroFreight API",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### GET /prices/history
Retorna histórico de preços.

**Query Parameters:**
```json
{
  "commodity": "soybean | fertilizer | freight",
  "date_from": "ISO8601",
  "date_to": "ISO8601",
  "granularity": "hour | day | week (default: day)"
}
```

**Response 200:**
```json
{
  "commodity": "soybean",
  "data": [
    {
      "timestamp": "2024-01-15T00:00:00Z",
      "price_r_sc": 185.50,
      "source": "CEPEA/ESALQ"
    }
  ]
}
```

### POST /prices/refresh
Força atualização de preços (admin only).

**Response 200:**
```json
{
  "status": "success",
  "updated_commodities": ["soybean", "fertilizer", "freight"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 4. Upload de Dados

### POST /upload/validate
Valida arquivo antes do upload.

**Request (multipart/form-data):**
```
file: <arquivo>
format: csv | xlsx | geojson | shapefile
```

**Response 200:**
```json
{
  "valid": true,
  "total_rows": 245,
  "errors": [],
  "warnings": [
    {
      "row": 12,
      "field": "moisture_pct",
      "message": "Umidade acima de 20% pode indicar problema na colheita"
    }
  ],
  "suggested_mapping": {
    "field_id": "field_id",
    "area_ha": "area_hectares",
    "planting_date": "data_plantio",
    "variety": "variedade",
    "yield_kg_ha": "produtividade_kg_ha"
  }
}
```

### POST /upload/ingest
Faz upload e ingestão de dados.

**Request:**
```json
{
  "file_id": "uuid",
  "column_mapping": {
    "field_id": "field_id",
    "area_ha": "area_hectares",
    "planting_date": "data_plantio"
  },
  "options": {
    "create_fields": true,
    "version": "2024-01-15"
  }
}
```

**Response 202:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "estimated_time_seconds": 30
}
```

### GET /upload/status/{job_id}
Verifica status do job de ingestão.

**Response 200:**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "progress": 100,
  "records_imported": 245,
  "records_failed": 1,
  "errors": [
    {
      "row": 12,
      "error": "Data inválida"
    }
  ]
}
```

---

## 5. Simulação What-If

### POST /simulations/what-if
Cria simulação de cenário.

**Request:**
```json
{
  "field_id": 1,
  "scenario": {
    "rainfall_mm": 850,
    "soybean_price_r_sc": 170.0,
    "fertilizer_n_kg_ha": 80,
    "planting_date": "2024-10-15"
  },
  "model_version": "v2.1"
}
```

**Response 200:**
```json
{
  "simulation_id": "uuid",
  "field_id": 1,
  "baseline": {
    "productivity_kg_ha": 3450.2,
    "yield_t": 4.312,
    "margin_r_ha": 2100.0
  },
  "projected": {
    "productivity_kg_ha": 3680.5,
    "yield_t": 4.600,
    "margin_r_ha": 2450.0,
    "delta_pct": {
      "productivity": 6.7,
      "yield": 6.7,
      "margin": 16.7
    }
  },
  "explainability": {
    "shap_values": {
      "rainfall": 12.3,
      "price": 8.1,
      "fertilizer_n": 5.2
    }
  },
  "computation_time_ms": 1250
}
```

---

## 6. Previsão e Modelos

### GET /predictions/{field_id}
Retorna previsão de produtividade.

**Query Parameters:**
```json
{
  "horizon_days": "integer (default: 30)",
  "include_intervals": "boolean (default: true)"
}
```

**Response 200:**
```json
{
  "field_id": 1,
  "model_version": "v2.1",
  "prediction": {
    "productivity_kg_ha": 3450.2,
    "confidence_interval_95": {
      "lower": 3200.0,
      "upper": 3700.0
    }
  },
  "features_used": {
    "ndvi_t": 0.72,
    "rainfall_mm": 920,
    "soil_ph": 6.2,
    "planting_date": "2024-10-20",
    "inputs_n_kg_ha": 120
  }
}
```

---

## 7. Planejamento de Colheita

### GET /harvest/plan
Retorna plano de colheita (GANTT).

**Query Parameters:**
```json
{
  "season": "string",
  "farm_id": "integer (optional)"
}
```

**Response 200:**
```json
{
  "season": "2024/2025",
  "schedule": [
    {
      "field_id": 1,
      "field_name": "Talhão 1",
      "start_date": "2025-01-15",
      "end_date": "2025-01-20",
      "harvester": "Colheitadeira A",
      "estimated_yield_t": 4.312
    }
  ]
}
```

### POST /harvest/optimize-routes
Otimiza rotas de colheita (VRP).

**Request:**
```json
{
  "fields": [1, 3, 4],
  "silo_location": {
    "coordinates": [-55.95, -12.55]
  },
  "harvesters": [
    {
      "id": "harvester_a",
      "capacity_t": 10.0
    }
  ]
}
```

**Response 200:**
```json
{
  "routes": [
    {
      "harvester_id": "harvester_a",
      "sequence": [
        {"field_id": 1, "arrival_time": "2025-01-15T08:00:00Z"},
        {"field_id": 3, "arrival_time": "2025-01-15T12:00:00Z"},
        {"field_id": 4, "arrival_time": "2025-01-15T16:00:00Z"}
      ],
      "total_distance_km": 35.0,
      "total_time_hours": 2.25,
      "total_cost_r": 280.0
    }
  ]
}
```

---

## 8. Relatórios e Exportação

### POST /reports/generate
Gera relatório customizado.

**Request:**
```json
{
  "template": "summary | detailed | map",
  "fields": [1, 3, 4],
  "format": "pdf | csv | xlsx | geojson | shapefile",
  "options": {
    "include_map": true,
    "watermark": true,
    "digital_signature": false
  }
}
```

**Response 202:**
```json
{
  "report_id": "uuid",
  "status": "generating",
  "estimated_time_seconds": 45
}
```

### GET /reports/{report_id}/download
Download do relatório gerado.

**Response 200:**
```
Content-Type: application/pdf (ou outro formato)
[Binary data]
```

---

## WebSocket - Atualizações em Tempo Real

### WS /ws/prices
Stream de atualizações de preços.

**Message (Server → Client):**
```json
{
  "type": "price_update",
  "commodity": "soybean",
  "price_r_sc": 185.50,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### WS /ws/alerts
Stream de alertas fitossanitários.

**Message (Server → Client):**
```json
{
  "type": "alert",
  "field_id": 1,
  "alert_type": "disease",
  "severity": "high",
  "message": "Ferrugem detectada"
}
```

---

## Códigos de Erro

- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Token inválido/expirado
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Recurso não encontrado
- `429 Too Many Requests`: Rate limit excedido
- `500 Internal Server Error`: Erro do servidor
- `503 Service Unavailable`: Serviço temporariamente indisponível


