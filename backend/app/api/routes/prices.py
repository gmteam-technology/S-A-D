import json
import logging
from datetime import datetime, timedelta
from typing import Optional

import redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

# Configuração Redis (ajustar conforme necessário)
# Tenta criar conexão Redis, mas não falha se não estiver disponível
redis_client: redis.Redis | None = None
try:
    redis_client = redis.from_url(
        settings.redis_url,
        socket_connect_timeout=1,
        socket_timeout=1,
        decode_responses=True,
        health_check_interval=30
    )
except Exception as e:
    logger.warning(f"Redis não está disponível para cache de preços: {e}. Cache desabilitado.")
    redis_client = None

CACHE_TTL = 300  # 5 minutos


async def fetch_cepea_soybean_price() -> Optional[dict]:
    """
    Busca preço de soja do CEPEA/ESALQ.
    Em produção, implementar chamada real à API.
    """
    try:
        # Mock - implementar chamada real
        return {
            "price_r_sc": 185.50,
            "price_r_t": 3108.33,  # 185.50 * 16.67
            "source": "CEPEA/ESALQ",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Erro ao buscar CEPEA: {e}")
        return None


async def fetch_b3_contract_price() -> Optional[dict]:
    """
    Busca preço de contrato da B3.
    """
    try:
        # Mock - implementar chamada real
        return {
            "price_r_sc": 188.20,
            "maturity": "2025-03",
            "source": "B3",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Erro ao buscar B3: {e}")
        return None


async def fetch_fertilizer_price() -> Optional[dict]:
    """
    Busca preço de fertilizante.
    """
    try:
        # Mock - implementar chamada real
        return {
            "price_r_t": 3450.00,
            "source": "ANDA",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Erro ao buscar fertilizante: {e}")
        return None


async def fetch_freight_price() -> Optional[dict]:
    """
    Busca preço de frete.
    """
    try:
        # Mock - implementar chamada real
        return {
            "price_r_t": 85.00,
            "route": "Fazenda → Port",
            "distance_km": 120,
            "source": "AgroFreight API",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Erro ao buscar frete: {e}")
        return None


@router.get("/current")
async def get_current_prices(
    commodity: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Retorna preços atuais (com cache de 5 minutos).
    """
    results = {}
    
    # Soja Spot
    cache_key_spot = "price:soybean:spot"
    spot_data = None
    
    if redis_client:
        try:
            cached = redis_client.get(cache_key_spot)
            if cached:
                spot_data = json.loads(cached)
        except Exception as e:
            logger.warning(f"Erro ao ler cache Redis para soja spot: {e}")
    
    if not spot_data:
        spot_data = await fetch_cepea_soybean_price()
        if spot_data and redis_client:
            try:
                redis_client.setex(cache_key_spot, CACHE_TTL, json.dumps(spot_data))
            except Exception as e:
                logger.warning(f"Erro ao escrever cache Redis para soja spot: {e}")
    
    if spot_data:
        results["soybean"] = {
            "spot": {
                **spot_data,
                "last_updated": spot_data["timestamp"],
                "cache_ttl_seconds": CACHE_TTL
            }
        }
    
    # Soja Contrato
    cache_key_contract = "price:soybean:contract"
    contract_data = None
    
    if redis_client:
        try:
            cached = redis_client.get(cache_key_contract)
            if cached:
                contract_data = json.loads(cached)
        except Exception as e:
            logger.warning(f"Erro ao ler cache Redis para soja contrato: {e}")
    
    if not contract_data:
        contract_data = await fetch_b3_contract_price()
        if contract_data and redis_client:
            try:
                redis_client.setex(cache_key_contract, CACHE_TTL, json.dumps(contract_data))
            except Exception as e:
                logger.warning(f"Erro ao escrever cache Redis para soja contrato: {e}")
    
    if contract_data:
        if "soybean" not in results:
            results["soybean"] = {}
        results["soybean"]["contract"] = contract_data
    
    # Fertilizante
    cache_key_fertilizer = "price:fertilizer:npk"
    fertilizer_data = None
    
    if redis_client:
        try:
            cached = redis_client.get(cache_key_fertilizer)
            if cached:
                fertilizer_data = json.loads(cached)
        except Exception as e:
            logger.warning(f"Erro ao ler cache Redis para fertilizante: {e}")
    
    if not fertilizer_data:
        fertilizer_data = await fetch_fertilizer_price()
        if fertilizer_data and redis_client:
            try:
                redis_client.setex(cache_key_fertilizer, CACHE_TTL, json.dumps(fertilizer_data))
            except Exception as e:
                logger.warning(f"Erro ao escrever cache Redis para fertilizante: {e}")
    
    if fertilizer_data:
        results["fertilizer"] = {"npk_10_10_10": fertilizer_data}
    
    # Frete
    cache_key_freight = "price:freight"
    freight_data = None
    
    if redis_client:
        try:
            cached = redis_client.get(cache_key_freight)
            if cached:
                freight_data = json.loads(cached)
        except Exception as e:
            logger.warning(f"Erro ao ler cache Redis para frete: {e}")
    
    if not freight_data:
        freight_data = await fetch_freight_price()
        if freight_data and redis_client:
            try:
                redis_client.setex(cache_key_freight, CACHE_TTL, json.dumps(freight_data))
            except Exception as e:
                logger.warning(f"Erro ao escrever cache Redis para frete: {e}")
    
    if freight_data:
        results["freight"] = freight_data
    
    if not results:
        raise HTTPException(status_code=503, detail="Serviço de preços temporariamente indisponível")
    
    return results


@router.post("/refresh")
async def refresh_prices(
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Força atualização de preços (admin only).
    """
    # Limpar cache
    if redis_client:
        try:
            redis_client.delete("price:soybean:spot")
            redis_client.delete("price:soybean:contract")
            redis_client.delete("price:fertilizer:npk")
            redis_client.delete("price:freight")
        except Exception as e:
            logger.warning(f"Erro ao limpar cache Redis: {e}")
    
    # Buscar novos preços
    prices = await get_current_prices(db=db)
    
    return {
        "status": "success",
        "updated_commodities": list(prices.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }

