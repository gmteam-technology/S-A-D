# Arquitetura do SIAD Agro

## Visão Geral
O SIAD Agro é um sistema completo de apoio à decisão para o agronegócio que integra dados de clima, solo, produtividade, custos, mapas e simulações para produtores, consultores e gestores. A solução é dividida em três blocos principais:

1. **Frontend** (React + Next.js + TypeScript, Tailwind e Framer Motion): PWA responsivo com dashboards em tempo real, mapas interativos e módulos de simulação.
2. **Backend** (FastAPI + PostgreSQL/PostGIS + Redis): API segura, escalável e observável com módulos especializados (clima, solo, safra, cenários, ETL e relatórios).
3. **Infraestrutura** (Docker Compose + GitHub Actions + Helm Charts): Provisiona ambientes de desenvolvimento e produção com observabilidade (OpenTelemetry, Prometheus, Grafana) e pipelines CI/CD.

## Justificativa das Tecnologias
| Camada | Tecnologia | Justificativa |
| --- | --- | --- |
| Frontend | Next.js + React 18 | Renderização híbrida, roteamento avançado, otimizações automáticas e suporte nativo a PWA e i18n. |
| Estado | Zustand + React Query | Zustand para estado global granular (ex.: RBAC e preferências) e React Query para cache de dados remotos e revalidação automática. |
| UI | TailwindCSS + Framer Motion + Recharts + React Leaflet | Permite design minimalista, animações suaves e mapas interativos com baixo esforço. |
| Backend | FastAPI + SQLAlchemy + Pydantic | Alto desempenho async, tipagem forte, geração automática do OpenAPI e fácil integração com workers e ML. |
| Banco | PostgreSQL + PostGIS | Requerido para análises geoespaciais e consultas de talhões. |
| Cache | Redis | Acelera previsões climáticas, sessões e locks de ETL. |
| Armazenamento | MinIO (compatível S3) | Uploads seguros de CSV/XLSX/GeoTIFF com versionamento. |
| Mensageria | Redis Streams / Celery | Orquestra ingestões e simulações assíncronas. |
| Observabilidade | OpenTelemetry + Prometheus + Grafana + Loki | Tracing distribuído, métricas e logs estruturados JSON. |

## Módulos do Backend
- **Auth & RBAC**: JWT + refresh tokens, roles (produtor, agrônomo, gestor, visualizador), auditoria de ações com trilhas de logs.
- **Weather**: rotas `/weather/forecast`, `/weather/history`, `/weather/stations`; integra APIs externas e aplica modelos ARIMA/Prophet simplificados.
- **Crops/Safras**: planejamento, produtividade, custos, simulações multi-variáveis e relatórios.
- **Scenarios**: motor what-if com parâmetros de chuva, insumos, cultivar, densidade e preços.
- **Soil**: análises químicas (pH, MO, NPK), recomendações de adubação, mapas de solo/drenagem.
- **Fields & Maps**: CRUD de talhões, camadas NDVI/solo/clima, cálculo de áreas com PostGIS.
- **Inputs & Costs**: inventário de insumos, custo por hectare, margem e sensibilidade.
- **Reports**: exportação PDF/CSV com templates modulares (WeasyPrint) e dispatcher assíncrono.
- **ETL/Ingestão**: pipelines para CSV/XLSX/JSON, validação, normalização e integração com GeoTIFF.

## Fluxo de Dados
```mermaid
graph LR
  subgraph Usuários
    UI[Frontend PWA]
  end
  subgraph Backend (FastAPI)
    API[(Gateways)] --> AUTH
    API --> WEATHER
    API --> CROPS
    API --> SCENARIOS
    API --> SOIL
    API --> FIELDS
    API --> REPORTS
    API --> ETL
  end
  subgraph Infra
    PG[(PostgreSQL + PostGIS)]
    REDIS[(Redis Cache)]
    MINIO[(MinIO S3)]
    PROM[(Prometheus/Grafana)]
  end
  UI <--> API
  WEATHER --> PG
  WEATHER --> REDIS
  CROPS --> PG
  SCENARIOS --> PG
  SCENARIOS --> REDIS
  SOIL --> PG
  FIELDS --> PG
  ETL --> MINIO
  ETL --> PG
  REPORTS --> MINIO
  API -. tracing .-> PROM
```

## Segurança
- JWT assinado com rotacionamento e refresh tokens armazenados em Redis com TTL.
- Rate limiting por IP/usuário com Redis.
- Sanitização e validação com Pydantic + `python-rapidjson` para inputs grandes.
- Helmet/CORS configurados no FastAPI + Next.js.
- OWASP Top 10 tratado com: parametrização SQL, CSRF (tokens em formulários sensíveis), CSP estrita e auditoria de logs.

## Modelos Analíticos
- **Previsão de produtividade**: regressão multivariada (chuva acumulada, NDVI médio, custo de insumos, cultivar) + ajuste ARIMA para ruído temporal.
- **Previsão climática**: modelo SARIMAX com dados meteorológicos locais, fallback para média histórica.
- **NDVI**: cálculo local `NDVI = (NIR - RED) / (NIR + RED)` com rasterio para GeoTIFFs.
- **Simulação**: Monte Carlo simplificado combinando solo × clima × insumos × cultivar com 5.000 iterações e distribuição triangular para preços.

## Frontend
- **Layout**: shell com dashboard principal, módulos (Clima, Safras, Cenários, Mapas, ETL, Relatórios), suporte a dark mode e i18n (pt-BR/en-US).
- **Componentes chave**: cards animados, widgets drag & drop (React Grid Layout), gráficos (Recharts + Framer Motion), mapa Leaflet com desenho de polígonos e camadas, formulários de cenários, wizard de upload ETL, gerador de relatórios.
- **Estado**: Zustand para tema/RBAC, React Query para dados assíncronos com streaming SSE para simulações.
- **Testes**: Jest + React Testing Library, Cypress para E2E e axe-core para acessibilidade.

## Infraestrutura e Deploy
- **docker-compose**: serviços `frontend`, `backend`, `postgres`, `redis`, `minio`, `otel-collector`, `prometheus`, `grafana`.
- **CI/CD (GitHub Actions)**:
  1. Lint (ESLint, mypy, Ruff)
  2. Testes (Jest, Pytest, Cypress component headless)
  3. Build (Docker multi-stage)
  4. Deploy (Helm chart para Kubernetes ou Cloud Run).
- **Observabilidade**: OpenTelemetry integrado no FastAPI e Next.js, métricas expostas via `/metrics` e dashboards Helm pré-configurados.

## Próximos Passos
1. Gerar scaffolding do backend (FastAPI + SQLAlchemy + Alembic).
2. Criar frontend com Next.js, Tailwind, Framer Motion e Leaflet.
3. Implementar pipelines ETL, seeds e arquivos de exemplo.
4. Configurar docker-compose, scripts de inicialização e documentação operacional.
5. Automatizar testes, CI/CD e checklist final.
