#!/bin/bash
set -e

echo "Aguardando banco de dados estar pronto..."
MAX_RETRIES=30
RETRY_COUNT=0

# Extrai host e porta da URL de conexão
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if poetry run python -c "
import sys
try:
    import psycopg
    conn = psycopg.connect('host=${DB_HOST} port=${DB_PORT} user=siad password=siad dbname=siad connect_timeout=2')
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
    echo "Banco de dados está pronto!"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "Tentativa $RETRY_COUNT/$MAX_RETRIES: Banco de dados ainda não está pronto. Aguardando..."
  sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "ERRO: Não foi possível conectar ao banco de dados após $MAX_RETRIES tentativas"
  exit 1
fi

echo "Executando migrações do Alembic..."
set +e  # Permite continuar mesmo se alembic falhar
poetry run alembic upgrade head
ALEMBIC_EXIT=$?
set -e  # Reativa o modo de erro
if [ $ALEMBIC_EXIT -ne 0 ]; then
  echo "AVISO: Falha ao executar migrações (código: $ALEMBIC_EXIT). Continuando mesmo assim..."
fi

echo "Iniciando servidor..."
exec "$@"

