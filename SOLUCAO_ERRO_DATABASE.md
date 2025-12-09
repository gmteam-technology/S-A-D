# Solução para Erro de Conexão com PostgreSQL

## Problema
O erro `OSError: Multiple exceptions: [Errno 10061] Connect call failed` indica que o backend não consegue conectar ao PostgreSQL na porta 5432.

## Soluções

### Opção 1: Usar Docker Compose (Recomendado)

#### Passo 1: Iniciar o Docker Desktop
Certifique-se de que o Docker Desktop está rodando no Windows.

#### Passo 2: Subir apenas os serviços de infraestrutura
Na raiz do projeto, execute:

```bash
docker-compose up -d postgres redis minio
```

Isso vai subir:
- PostgreSQL/PostGIS na porta 5432
- Redis na porta 6379
- MinIO nas portas 9000 e 9001

#### Passo 3: Aguardar o PostgreSQL ficar pronto
Aguarde alguns segundos para o PostgreSQL inicializar completamente. Você pode verificar com:

```bash
docker-compose ps
```

#### Passo 4: Rodar as migrações
No diretório `backend`, execute:

```bash
cd backend
poetry run alembic upgrade head
```

#### Passo 5: Popular o banco (opcional)
```bash
poetry run seed run
```

#### Passo 6: Rodar o backend
```bash
poetry run uvicorn app.main:app --reload
```

### Opção 2: Instalar PostgreSQL Localmente

#### Passo 1: Instalar PostgreSQL com PostGIS
1. Baixe o PostgreSQL: https://www.postgresql.org/download/windows/
2. Durante a instalação, instale também a extensão PostGIS
3. Configure uma senha para o usuário `postgres`

#### Passo 2: Criar o banco de dados
Abra o pgAdmin ou use o psql:

```sql
CREATE DATABASE siad;
CREATE USER siad WITH PASSWORD 'siad';
GRANT ALL PRIVILEGES ON DATABASE siad TO siad;
```

#### Passo 3: Habilitar PostGIS
Conecte ao banco `siad` e execute:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

#### Passo 4: Configurar variáveis de ambiente
Crie um arquivo `backend/.env` baseado no `backend/.env.example`:

```env
DATABASE_URL=postgresql+asyncpg://siad:siad@localhost:5432/siad
SYNC_DATABASE_URL=postgresql+psycopg://siad:siad@localhost:5432/siad
```

#### Passo 5: Rodar migrações e backend
```bash
cd backend
poetry run alembic upgrade head
poetry run seed run
poetry run uvicorn app.main:app --reload
```

### Opção 3: Rodar tudo com Docker Compose

Se preferir rodar tudo junto (backend, frontend e serviços):

```bash
docker-compose up --build
```

Isso vai subir todos os serviços. O backend estará disponível em `http://localhost:8000`.

## Verificar se está funcionando

Após seguir uma das opções acima, teste:

1. Acesse `http://localhost:8000/docs` para ver a documentação da API
2. Acesse `http://localhost:8000/healthz` para verificar o healthcheck

## Comandos úteis

### Parar os serviços Docker
```bash
docker-compose down
```

### Ver logs dos serviços
```bash
docker-compose logs -f postgres
```

### Verificar status dos containers
```bash
docker-compose ps
```

### Limpar volumes (cuidado: apaga dados)
```bash
docker-compose down -v
```

