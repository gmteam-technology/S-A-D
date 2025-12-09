# SIAD Agro – Sistema de Informação de Apoio à Decisão

Plataforma full-stack para agricultores, consultores e gestores com dashboards inteligentes, módulos de clima/solo, simulações de safra, mapa interativo, ETL agrícola e relatórios exportáveis. O projeto inclui frontend (Next.js + Tailwind + Framer Motion + React Query + Zustand), backend FastAPI com PostgreSQL/PostGIS, Redis e MinIO, além de pipelines ETL, seeds, testes e infraestrutura pronta para Docker/Kubernetes.

## Estrutura do repositório
```
backend/   # FastAPI, SQLAlchemy, Celery, seeds, testes
frontend/  # Next.js 16 (App Router), Tailwind, Framer Motion, PWA, Jest, Cypress
data/      # Amostras (produtividade, chuva, GeoJSON, planilha de custos)
docs/      # Arquitetura, OpenAPI, diagramas
ops/       # Configurações de observabilidade (OpenTelemetry collector)
```

## Como rodar com Docker Compose
```bash
docker-compose up --build
```
Serviços expostos:
- Frontend: http://localhost:3000
- Backend/API: http://localhost:8000
- Postgres/PostGIS: 5432
- Redis: 6379
- MinIO: http://localhost:9000 (console: :9001)

## Execução manual
### Backend

**⚠️ Requisito de Python:** O projeto requer Python 3.11 ou 3.12. Python 3.13 não é suportado devido à falta de wheels pré-compilados para alguns pacotes (pyarrow, asyncpg) no Windows.

```bash
cd backend
poetry install
poetry run alembic upgrade head
poetry run seed run
poetry run uvicorn app.main:app --reload
```

**Nota sobre Python 3.13:** Se você estiver usando Python 3.13 e encontrar erros de compilação, você tem duas opções:
1. **Recomendado:** Use Python 3.11 ou 3.12 (conforme especificado no `pyproject.toml`)
2. **Alternativa:** Instale o Microsoft Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Defina `NEXT_PUBLIC_API_URL=http://localhost:8000` no `.env.local`.

## Testes e qualidade
- Backend: `poetry run pytest`
- Frontend unit + acessibilidade: `npm test`
- Lint: `poetry run ruff check && npm run lint`
- E2E: `npm run test:e2e`

## Funcionalidades principais
- Dashboards animados com cards, gráficos (Recharts) e widgets drag & drop.
- Módulo de cenários what-if com simulações (chuva, insumos, cultivar, preço).
- Módulo climatológico: previsão de 7 dias, histograma de chuva, radar e indicadores (ETo, NDVI, Kc).
- Módulo de safras: planejamento, custos, produtividade histórica e comparativos.
- Mapa Agro (Leaflet) com desenho de talhões, camadas solo/NDVI/clima, upload GeoJSON/CSV, validação PostGIS.
- ETL/Uploads: CSV, XLSX, JSON e GeoTIFF (integração opcional) com limpeza automática e mapeamento.
- Relatórios exportáveis (PDF/CSV) de safra, clima, custos, previsões e mapas.
- Auth + RBAC (produtor, agrônomo, gestor, visualizador), tokens JWT/refresh, auditoria e rate limiting.
- APIs completas (`/weather/*`, `/crops/*`, `/scenarios/*`, `/soil/*`, `/fields/*`, `/inputs/*`, `/reports`, `/etl`).
- Modelos analíticos: ARIMA/SARIMAX simplificados, regressão para produtividade e cálculo NDVI local.
- Documentação OpenAPI em `docs/openapi.yaml` + diagramas mermaid em `docs/ARCHITECTURE.md`.
- Seeds com >200 linhas (`backend/app/scripts/seed.py`) + dados reais em `data/samples`.

## CI/CD
Workflow GitHub Actions (`.github/workflows/ci.yml`) roda lint + testes (backend/frontend) e build das imagens Docker. Observabilidade por OpenTelemetry + Prometheus/Grafana (via Helm) incluída na documentação.

## Próximos passos sugeridos
1. Conectar APIs externas de clima (INMET, NOAA) e satélite (Sentinel/Landsat) para alimentar `WeatherService`.
2. Implantar em Kubernetes usando Helm Charts (exemplo disponível no README backend) ou Cloud Run/ECS.
3. Configurar autenticação SSO (Keycloak/Cognito) e filas assíncronas com Celery + Redis Streams.
4. Expandir modelos preditivos com Prophet/XGBoost e incorporar GeoTIFF NDVI diretamente no ETL.
