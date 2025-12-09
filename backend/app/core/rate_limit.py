import logging
from fastapi import HTTPException, status
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Cria conexão Redis com timeout curto para não bloquear
redis: Redis | None = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
    retry_on_timeout=False,
    health_check_interval=30
)


async def enforce(identifier: str, limit: int = 120, ttl: int = 60) -> None:
    """
    Enforce rate limiting. Se Redis não estiver disponível, permite todas as requisições.
    Em desenvolvimento, rate limiting é opcional.
    """
    if not redis:
        return
    
    try:
        key = f"rate:{identifier}"
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, ttl)
        if count > limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Limite de requisições excedido")
    except (RedisConnectionError, OSError, Exception) as e:
        # Se houver erro de conexão, loga mas permite a requisição (especialmente em desenvolvimento)
        if settings.app_env == "development":
            logger.debug(f"Redis não disponível para rate limiting: {e}. Permitindo requisição em desenvolvimento.")
        else:
            logger.warning(f"Erro ao conectar com Redis durante rate limiting: {e}. Permitindo requisição.")
        # Não levanta exceção, permite que a requisição continue
