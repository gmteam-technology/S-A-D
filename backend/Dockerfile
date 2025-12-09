FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install --no-cache-dir poetry

# Configura variáveis de ambiente para aumentar timeouts e retries
ENV PIP_DEFAULT_TIMEOUT=300
ENV PIP_RETRIES=5
ENV POETRY_HTTP_TIMEOUT=300

# Configura Poetry para ser mais resiliente a falhas de rede
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 1 \
    && poetry config installer.no-binary false

# Copia e instala dependências Python (cache layer)
COPY pyproject.toml README.md ./

# Instala dependências com retry em caso de falha de rede
RUN poetry install --no-root --only main --no-interaction || \
    (echo "⚠️ Primeira tentativa falhou. Aguardando 15s e tentando novamente..." && \
     sleep 15 && \
     poetry install --no-root --only main --no-interaction) || \
    (echo "⚠️ Segunda tentativa falhou. Aguardando 30s e tentando uma última vez..." && \
     sleep 30 && \
     poetry install --no-root --only main --no-interaction)

# Copia código da aplicação
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

# Copia e configura entrypoint
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Cria diretório de storage
RUN mkdir -p /app/storage/uploads

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]