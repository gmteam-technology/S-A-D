# Guia Operacional e Checklist

## Checklist de Funcionamento
1. `docker-compose up --build` executado sem erros.
2. Backend responde em `http://localhost:8000/health/z`.
3. Login: use `gestor@siad.ag` + `admin123` (seed) → recebe JWT + refresh.
4. RBAC: endpoints `/fields` (gestor/produtor), `/reports` (gestor/agronomo) e `/weather/*` (todos) testados.
5. Upload CSV em `/etl/upload` com `data/samples/productivity.csv`.
6. Mapa Agro renderiza camadas e talhões (frontend → seção "Mapa Agro").
7. Simulação de safra via `/crops/simulation` retorna resultado coerente (teste com payload do README backend).
8. Relatório PDF concluído (`/reports` → status `finished`, arquivo em bucket MinIO).
9. Forecast climático responde dados seeded (`/weather/forecast?station=BR001`).
10. Cypress `npm run test:e2e` e Jest `npm test` passam.

## Execução Local com Banco Limpo
```bash
# Postgres + extensões
psql -h localhost -U siad -d siad -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
poetry run alembic upgrade head
poetry run seed run

# Frontend
npm run dev --workspace frontend
```

## Estratégia de Deploy (Helm/Kubernetes)
1. **Build das imagens**: `docker build -t registry/siad-backend ./backend` e `docker build -t registry/siad-frontend ./frontend`.
2. **Push**: `docker push registry/siad-backend` e `docker push registry/siad-frontend`.
3. **Helm chart** (exemplo):
   - `values.yaml` define secrets (JWT, banco, MinIO), réplicas, HPA e serviços.
   - Incluir `ServiceMonitor` para Prometheus e `PodMonitor` para Otel Collector.
4. **Apply**: `helm upgrade --install siad charts/siad -n siad --create-namespace`.
5. **Monitoramento**: dashboards no Grafana (NDVI, margem, latência API) e traces no Tempo/Jaeger.

## Observabilidade
- **Traces**: FastAPI e SQLAlchemy instrumentados (OpenTelemetry). Exportador OTLP → Collector (`ops/otel-collector-config.yaml`).
- **Logs**: Loguru (JSON) + stack Promtail/Loki opcional.
- **Métricas**: `/metrics` (Prometheus). Inclui latência, contagem de cenários, consumo ETL.

## Segurança
- JWT + refresh + Redis (lista de refresh). Rotação recomendada a cada 30 dias.
- Rate limiting (Redis) com política 120 req/min por usuário.
- Sanitização de uploads ETL (Pandas + validação schema). GeoJSON validado via Shapely/PostGIS.
- OWASP mitigado com: cabeçalhos CORS restritos, CSP estrita, SQL parametrizado e auditoria (`AuditLog`).

## ETL Pipeline
1. ETL API recebe arquivo → salva temporariamente em `storage/uploads`.
2. Pandas valida cabeçalho, normaliza chuva/NDVI/solo.
3. GeoJSON validado com Shapely;, MultiPolygon convertido para SRID 4674 antes de persistir.
4. Trace do job registrado no Redis Streams para monitoria.

## Relatórios
- `ReportService` gera PDF com ReportLab (templates modulares). Disponível via S3/MinIO.
- CSV exportado diretamente dos dataframes (chuva, custos, NDVI).

## Scripts Úteis
- `poetry run seed run`: popula usuários, estações, talhões, cenários e insumos.
- `poetry run etl run data/samples/productivity.csv`: executa pipeline CLI.

> Consulte `docs/ARCHITECTURE.md` para diagramas Mermaid e visão macro da solução.
