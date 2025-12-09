# Scripts de Exemplo - Sistema de Gestão de Safra

## 1. Ingestão GeoJSON → PostGIS

```python
"""
Script: ingest_geojson_to_postgis.py
Descrição: Importa talhões de um arquivo GeoJSON para PostGIS
"""

import json
import psycopg2
from psycopg2.extras import execute_values
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuração
DATABASE_URL = "postgresql://user:pass@localhost:5432/siad"
GEOJSON_FILE = "data/talhoes.geojson"

def ingest_geojson_to_postgis(geojson_file: str, db_url: str):
    """
    Ingere arquivo GeoJSON no PostGIS.
    
    Schema esperado:
    - field_id: integer
    - name: string
    - area_ha: float
    - variety: string (opcional)
    - planting_date: date (opcional)
    """
    
    # Conectar ao banco
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Ler GeoJSON
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    features = geojson_data.get('features', [])
    
    # Preparar dados
    fields_data = []
    for feature in features:
        props = feature.get('properties', {})
        geometry = feature.get('geometry')
        
        # Validar campos obrigatórios
        if 'field_id' not in props:
            print(f"⚠️ Feature sem field_id, pulando...")
            continue
        
        # Converter geometria para WKT
        geom_wkt = json.dumps(geometry)
        
        fields_data.append({
            'field_id': props['field_id'],
            'name': props.get('name', f"Talhão {props['field_id']}"),
            'area_ha': props.get('area_ha', 0.0),
            'variety': props.get('variety'),
            'planting_date': props.get('planting_date'),
            'geometry': geom_wkt,
            'created_at': datetime.utcnow()
        })
    
    # Inserir no banco usando ST_GeomFromGeoJSON
    insert_query = """
        INSERT INTO fields (
            field_id, name, area_ha, variety, planting_date, geometry, created_at
        )
        VALUES (
            %(field_id)s, %(name)s, %(area_ha)s, %(variety)s, 
            %(planting_date)s, 
            ST_GeomFromGeoJSON(%(geometry)s), 
            %(created_at)s
        )
        ON CONFLICT (field_id) 
        DO UPDATE SET
            name = EXCLUDED.name,
            area_ha = EXCLUDED.area_ha,
            variety = EXCLUDED.variety,
            planting_date = EXCLUDED.planting_date,
            geometry = EXCLUDED.geometry,
            updated_at = NOW()
    """
    
    # Executar inserção
    with engine.connect() as conn:
        for field in fields_data:
            conn.execute(text(insert_query), field)
        conn.commit()
    
    print(f"✅ {len(fields_data)} talhões importados com sucesso!")
    session.close()

if __name__ == "__main__":
    ingest_geojson_to_postgis(GEOJSON_FILE, DATABASE_URL)
```

---

## 2. Chamada de API de Preços + Normalização + Cache

```python
"""
Script: fetch_prices_with_cache.py
Descrição: Busca preços de APIs oficiais, normaliza, valida e armazena em cache Redis
"""

import requests
import redis
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import statistics
from dataclasses import dataclass

# Configuração
REDIS_URL = "redis://localhost:6379/0"
CACHE_TTL_SECONDS = 300  # 5 minutos
CEPEA_API_URL = "https://api.cepea.esalq.usp.br/soja/preco"
B3_API_URL = "https://www.b3.com.br/api/precos/contratos"
ANDA_API_URL = "https://api.anda.org.br/fertilizantes/precos"

@dataclass
class PriceData:
    """Estrutura normalizada de preço"""
    commodity: str
    price_r_sc: Optional[float] = None
    price_r_t: Optional[float] = None
    source: str
    timestamp: datetime
    unit: str = "sc"  # sc (saca) ou t (tonelada)

class PriceFetcher:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
        self.cache_ttl = CACHE_TTL_SECONDS
    
    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Busca do cache Redis"""
        cached = self.redis_client.get(key)
        if cached:
            data = json.loads(cached)
            # Converter timestamp de volta para datetime
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            return data
        return None
    
    def _set_cache(self, key: str, data: Dict):
        """Armazena no cache Redis"""
        # Serializar datetime para ISO string
        serializable_data = data.copy()
        serializable_data['timestamp'] = data['timestamp'].isoformat()
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(serializable_data)
        )
    
    def _fetch_cepea_soybean_price(self) -> Optional[PriceData]:
        """Busca preço de soja do CEPEA/ESALQ"""
        try:
            response = requests.get(
                CEPEA_API_URL,
                headers={"Accept": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            # Normalizar: CEPEA retorna em R$/sc de 60kg
            price_r_sc = float(data.get('preco', 0))
            price_r_t = price_r_sc * 16.67  # 1t = 16.67 sacas de 60kg
            
            return PriceData(
                commodity="soybean",
                price_r_sc=price_r_sc,
                price_r_t=price_r_t,
                source="CEPEA/ESALQ",
                timestamp=datetime.utcnow(),
                unit="sc"
            )
        except Exception as e:
            print(f"❌ Erro ao buscar CEPEA: {e}")
            return None
    
    def _fetch_b3_contract_price(self) -> Optional[PriceData]:
        """Busca preço de contrato da B3"""
        try:
            response = requests.get(
                B3_API_URL,
                params={"commodity": "soybean", "maturity": "2025-03"},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            price_r_sc = float(data.get('preco_fechamento', 0))
            price_r_t = price_r_sc * 16.67
            
            return PriceData(
                commodity="soybean_contract",
                price_r_sc=price_r_sc,
                price_r_t=price_r_t,
                source="B3",
                timestamp=datetime.utcnow(),
                unit="sc"
            )
        except Exception as e:
            print(f"❌ Erro ao buscar B3: {e}")
            return None
    
    def _sanity_check(self, price: float, historical_prices: list) -> bool:
        """
        Validação de sanidade usando z-score.
        Rejeita valores que estão >3 desvios padrão da média histórica.
        """
        if not historical_prices or len(historical_prices) < 5:
            return True  # Sem histórico suficiente, aceita
        
        mean = statistics.mean(historical_prices)
        std_dev = statistics.stdev(historical_prices) if len(historical_prices) > 1 else 0
        
        if std_dev == 0:
            return True
        
        z_score = abs((price - mean) / std_dev)
        
        if z_score > 3:
            print(f"⚠️ Preço rejeitado por z-score alto: {z_score:.2f}")
            return False
        
        return True
    
    def fetch_and_cache_prices(self) -> Dict:
        """
        Busca preços, valida, normaliza e armazena em cache.
        Retorna dicionário com preços atualizados.
        """
        results = {}
        
        # 1. Soja Spot (CEPEA)
        cache_key_spot = "price:soybean:spot"
        cached_spot = self._get_from_cache(cache_key_spot)
        
        if cached_spot:
            print("✅ Preço spot do cache")
            results['soybean_spot'] = cached_spot
        else:
            price_data = self._fetch_cepea_soybean_price()
            if price_data:
                # Buscar histórico para validação
                historical = self._get_price_history("soybean_spot", days=30)
                historical_prices = [h['price_r_sc'] for h in historical]
                
                if self._sanity_check(price_data.price_r_sc, historical_prices):
                    price_dict = {
                        'price_r_sc': price_data.price_r_sc,
                        'price_r_t': price_data.price_r_t,
                        'source': price_data.source,
                        'timestamp': price_data.timestamp
                    }
                    self._set_cache(cache_key_spot, price_dict)
                    results['soybean_spot'] = price_dict
                    print(f"✅ Preço spot atualizado: R$ {price_data.price_r_sc:.2f}/sc")
                else:
                    print("⚠️ Preço spot rejeitado na validação")
        
        # 2. Soja Contrato (B3)
        cache_key_contract = "price:soybean:contract"
        cached_contract = self._get_from_cache(cache_key_contract)
        
        if cached_contract:
            print("✅ Preço contrato do cache")
            results['soybean_contract'] = cached_contract
        else:
            price_data = self._fetch_b3_contract_price()
            if price_data:
                price_dict = {
                    'price_r_sc': price_data.price_r_sc,
                    'price_r_t': price_data.price_r_t,
                    'source': price_data.source,
                    'timestamp': price_data.timestamp
                }
                self._set_cache(cache_key_contract, price_dict)
                results['soybean_contract'] = price_dict
                print(f"✅ Preço contrato atualizado: R$ {price_data.price_r_sc:.2f}/sc")
        
        return results
    
    def _get_price_history(self, commodity: str, days: int = 30) -> list:
        """Busca histórico de preços do banco de dados"""
        # Implementar busca no banco (TimescaleDB)
        # Por enquanto, retorna lista vazia
        return []

if __name__ == "__main__":
    fetcher = PriceFetcher(REDIS_URL)
    prices = fetcher.fetch_and_cache_prices()
    print(f"\n📊 Preços atualizados: {json.dumps(prices, indent=2, default=str)}")
```

---

## 3. Cálculo NDVI (Pseudo-código Python)

```python
"""
Script: calculate_ndvi.py
Descrição: Calcula NDVI a partir de bandas Sentinel-2 (B8 - NIR, B4 - Red)
"""

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.enums import Resampling as ResamplingEnum
import geopandas as gpd
from shapely.geometry import box

def calculate_ndvi_from_sentinel2(
    b8_path: str,  # Banda 8 (NIR - 842nm)
    b4_path: str,  # Banda 4 (Red - 665nm)
    output_path: str,
    field_geometry: gpd.GeoDataFrame = None,
    cloud_mask_path: str = None
) -> np.ndarray:
    """
    Calcula NDVI = (NIR - Red) / (NIR + Red)
    
    NDVI range: -1 a 1
    - < 0.3: Baixo vigor
    - 0.3 - 0.7: Médio vigor
    - > 0.7: Alto vigor
    """
    
    # 1. Carregar bandas
    with rasterio.open(b8_path) as nir_src:
        nir = nir_src.read(1).astype(np.float32)
        nir_profile = nir_src.profile
        nir_bounds = nir_src.bounds
    
    with rasterio.open(b4_path) as red_src:
        red = red_src.read(1).astype(np.float32)
        red_profile = red_src.profile
        red_bounds = red_src.bounds
    
    # 2. Reprojetar se necessário (garantir mesmo CRS e resolução)
    if nir_profile['crs'] != red_profile['crs']:
        # Reprojetar red para CRS do NIR
        red_reprojected = np.zeros_like(nir)
        reproject(
            source=rasterio.band(red_src, 1),
            destination=red_reprojected,
            src_crs=red_profile['crs'],
            dst_crs=nir_profile['crs'],
            resampling=Resampling.bilinear
        )
        red = red_reprojected
    
    # 3. Aplicar máscara de nuvem (se disponível)
    if cloud_mask_path:
        with rasterio.open(cloud_mask_path) as cloud_src:
            cloud_mask = cloud_src.read(1) == 0  # 0 = sem nuvem
            nir = np.where(cloud_mask, nir, np.nan)
            red = np.where(cloud_mask, red, np.nan)
    
    # 4. Calcular NDVI
    # Evitar divisão por zero
    denominator = nir + red
    ndvi = np.where(
        denominator != 0,
        (nir - red) / denominator,
        np.nan
    )
    
    # 5. Aplicar máscara de talhão (se fornecido)
    if field_geometry is not None:
        # Criar máscara raster do polígono do talhão
        from rasterio.features import geometry_mask
        mask = geometry_mask(
            field_geometry.geometry,
            out_shape=nir.shape,
            transform=nir_profile['transform'],
            invert=True
        )
        ndvi = np.where(mask, ndvi, np.nan)
    
    # 6. Aplicar smoothing (opcional - média móvel)
    from scipy.ndimage import uniform_filter
    ndvi_smoothed = uniform_filter(ndvi, size=3)
    ndvi = np.where(np.isnan(ndvi), ndvi, ndvi_smoothed)
    
    # 7. Salvar resultado
    output_profile = nir_profile.copy()
    output_profile.update({
        'dtype': 'float32',
        'nodata': np.nan,
        'compress': 'lzw'
    })
    
    with rasterio.open(output_path, 'w', **output_profile) as dst:
        dst.write(ndvi, 1)
    
    # 8. Estatísticas
    ndvi_valid = ndvi[~np.isnan(ndvi)]
    stats = {
        'mean': np.mean(ndvi_valid),
        'min': np.min(ndvi_valid),
        'max': np.max(ndvi_valid),
        'std': np.std(ndvi_valid),
        'pixels_valid': len(ndvi_valid),
        'pixels_total': ndvi.size
    }
    
    print(f"✅ NDVI calculado:")
    print(f"   Média: {stats['mean']:.3f}")
    print(f"   Min: {stats['min']:.3f}")
    print(f"   Max: {stats['max']:.3f}")
    print(f"   Pixels válidos: {stats['pixels_valid']}/{stats['pixels_total']}")
    
    return ndvi

def calculate_ndvi_timeseries(
    field_id: int,
    date_range: tuple,  # (start_date, end_date)
    output_dir: str
) -> list:
    """
    Calcula série temporal de NDVI para um talhão.
    Retorna lista de dicionários com data e estatísticas.
    """
    from datetime import datetime, timedelta
    
    start_date, end_date = date_range
    current_date = start_date
    timeseries = []
    
    while current_date <= end_date:
        # Buscar imagens Sentinel-2 para a data
        # (implementar busca na API Sentinel Hub ou similar)
        b8_path = f"sentinel2/{current_date:%Y%m%d}/B08.tif"
        b4_path = f"sentinel2/{current_date:%Y%m%d}/B04.tif"
        cloud_mask_path = f"sentinel2/{current_date:%Y%m%d}/cloud_mask.tif"
        
        if not (os.path.exists(b8_path) and os.path.exists(b4_path)):
            current_date += timedelta(days=10)  # Próxima imagem (Sentinel-2 revisita a cada 5 dias)
            continue
        
        # Calcular NDVI
        output_path = f"{output_dir}/ndvi_{field_id}_{current_date:%Y%m%d}.tif"
        ndvi = calculate_ndvi_from_sentinel2(
            b8_path, b4_path, output_path,
            cloud_mask_path=cloud_mask_path
        )
        
        # Estatísticas por talhão
        ndvi_valid = ndvi[~np.isnan(ndvi)]
        timeseries.append({
            'date': current_date.isoformat(),
            'ndvi_mean': float(np.mean(ndvi_valid)),
            'ndvi_min': float(np.min(ndvi_valid)),
            'ndvi_max': float(np.max(ndvi_valid)),
            'cloud_coverage_pct': float(np.sum(np.isnan(ndvi)) / ndvi.size * 100)
        })
        
        current_date += timedelta(days=10)
    
    return timeseries

if __name__ == "__main__":
    # Exemplo de uso
    ndvi = calculate_ndvi_from_sentinel2(
        b8_path="data/sentinel2/B08.tif",
        b4_path="data/sentinel2/B04.tif",
        output_path="output/ndvi.tif"
    )
```

---

## Notas de Implementação

### Ingestão GeoJSON
- Validar CRS (Coordinate Reference System) antes de inserir
- Criar índices espaciais (GIST) para performance
- Implementar versionamento de geometrias (audit trail)

### Preços
- Implementar fallback para múltiplas fontes
- Rate limiting: respeitar limites das APIs (ex: CEPEA permite 100 req/hora)
- Alertas quando preço varia >5% em 1 hora

### NDVI
- Processar em chunks para imagens grandes
- Usar Dask ou multiprocessing para paralelização
- Cache de resultados intermediários


