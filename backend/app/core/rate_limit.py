from fastapi import HTTPException, status
from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()
redis = Redis.from_url(settings.redis_url, decode_responses=True)


async def enforce(identifier: str, limit: int = 120, ttl: int = 60) -> None:
    key = f"rate:{identifier}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, ttl)
    if count > limit:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Limite de requisições excedido")
