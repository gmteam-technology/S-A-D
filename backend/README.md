# SIAD Backend (FastAPI)

## Visão Geral
Este backend fornece uma API robusta e segura para o Sistema de Informação de Apoio à Decisão (SIAD) no agronegócio. Ele consolida dados meteorológicos, de solo, produtividade, custos e mapas, oferecendo análises avançadas, simulações e relatórios exportáveis.

## Principais Recursos
- Autenticação JWT + refresh tokens e RBAC (produtor, agrônomo, gestor, visualizador).
- Endpoints para clima, solo, campos, safra, cenários, insumos, relatórios e ETL.
- Integração com PostgreSQL/PostGIS, Redis (cache e rate limiting) e MinIO (uploads S3).
- Pipelines de ingestão de CSV/XLSX/JSON com validação automática.
- Modelos de previsão (produtividade/clima), cálculo local de NDVI e simulações what-if.
- Observabilidade com OpenTelemetry + Prometheus, logs estruturados JSON, auditoria de eventos.

## Estrutura
```
backend/
├── app/
│   ├── api/            # Rotas organizadas por domínio
│   ├── core/           # Config, segurança, tracing, eventos
│   ├── db/             # Sessões, base models, seeds
│   ├── models/         # SQLAlchemy models (PostGIS)
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Clima, solo, cenários, relatórios etc
│   ├── tasks/          # Jobs Celery e ETL
│   ├── workers/        # Configuração Celery/Beat
│   ├── scripts/        # CLI Typer para seeds/ingestões
│   └── tests/          # Testes unitários e integração
├── alembic/            # Migrações de banco
├── pyproject.toml
└── README.md
```

## Variáveis de Ambiente
Crie `backend/.env` (vide `.env.example`):
```
APP_ENV=development
DATABASE_URL=postgresql+asyncpg://siad:siad@postgres:5432/siad
SYNC_DATABASE_URL=postgresql+psycopg://siad:siad@postgres:5432/siad
REDIS_URL=redis://redis:6379/0
S3_ENDPOINT=http://minio:9000
S3_BUCKET=siad-uploads
S3_ACCESS_KEY=siad
S3_SECRET_KEY=siad-secret
STORAGE_DIR=storage/uploads
JWT_SECRET=change-me
JWT_REFRESH_SECRET=change-me-too
OTLP_ENDPOINT=http://otel-collector:4317
```

## Execução Local
```bash
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

## Testes
```bash
poetry run pytest --asyncio-mode=auto --maxfail=1
```

## OpenAPI
Após subir o servidor, acesse `http://localhost:8000/docs` ou utilize o arquivo versionado em `docs/openapi.yaml`.

## Scripts Importantes
- `poetry run seed --dataset base` – popula dados mínimos (200+ linhas) em lote.
- `poetry run etl run data/samples/productivity.csv` – executa pipeline ETL.

## Docker
O `docker-compose.yml` na raiz orquestra backend, frontend, Postgres/PostGIS, Redis e MinIO. Utilize:
```bash
docker-compose up --build
```

## Observabilidade
- Métricas: `/metrics`
- Healthcheck: `/healthz`
- Tracing: enviado ao OpenTelemetry Collector configurado.
