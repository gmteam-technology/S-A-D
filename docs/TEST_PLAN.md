# Plano de Testes - Sistema de Gestão de Safra

## 1. Testes de Performance

### 1.1 Latência de APIs

**Objetivo:** Garantir que endpoints respondam dentro dos SLAs definidos.

| Endpoint | SLA | Método de Teste |
|----------|-----|-----------------|
| GET /dashboard/kpis | < 200ms | Load test com 100 req/s |
| GET /map/fields | < 500ms | Teste com 1000 talhões |
| GET /map/ndvi/{field_id} | < 1s | Teste com GeoTIFF de 100MB |
| GET /prices/current | < 50ms | Teste com cache hit |
| POST /simulations/what-if | < 2s | Teste com modelo carregado |

**Ferramentas:** k6, Locust, Apache Bench

**Script de Exemplo (k6):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% das requisições < 200ms
  },
};

export default function () {
  const res = http.get('https://api.siad-agro.com/v1/dashboard/kpis');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
```

---

### 1.2 Throughput

**Objetivo:** Sistema deve suportar 1000 requisições/segundo no pico.

**Teste:** 
- Ramp-up: 0 → 1000 req/s em 5 minutos
- Sustentar 1000 req/s por 10 minutos
- Ramp-down: 1000 → 0 req/s em 2 minutos

**Critérios de Aceitação:**
- Taxa de erro < 0.1%
- Latência p95 < 500ms
- CPU < 80%
- Memória < 80%

---

### 1.3 Processamento de Upload

**Objetivo:** Upload e processamento de arquivos grandes.

| Tipo de Arquivo | Tamanho | SLA |
|-----------------|---------|-----|
| CSV (10k linhas) | 5 MB | < 30s |
| XLSX (50k linhas) | 25 MB | < 2min |
| GeoJSON (100 features) | 10 MB | < 1min |
| Shapefile (50 MB) | 50 MB | < 5min |
| GeoTIFF (NDVI) | 500 MB | < 10min |

**Teste:**
```python
import requests
import time

def test_upload_performance(file_path, expected_time_seconds):
    start = time.time()
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'https://api.siad-agro.com/v1/upload/ingest',
            files=files,
            headers={'Authorization': 'Bearer TOKEN'}
        )
    
    elapsed = time.time() - start
    
    assert response.status_code == 202, "Upload falhou"
    assert elapsed < expected_time_seconds, f"Tempo excedido: {elapsed}s > {expected_time_seconds}s"
    
    job_id = response.json()['job_id']
    # Aguardar conclusão
    wait_for_job_completion(job_id)
    
    print(f"✅ Upload concluído em {elapsed:.2f}s")
```

---

## 2. Testes de Integração de Preços

### 2.1 Atualização a cada 5 minutos

**Objetivo:** Garantir que preços sejam atualizados corretamente a cada 5 minutos.

**Teste:**
```python
import time
import redis
from datetime import datetime, timedelta

def test_price_update_frequency():
    """Verifica se preços são atualizados a cada 5 minutos"""
    redis_client = redis.from_url("redis://localhost:6379/0")
    
    # Aguardar 6 minutos (1 minuto de margem)
    time.sleep(360)
    
    # Verificar timestamp do último update
    cached_price = redis_client.get("price:soybean:spot")
    if cached_price:
        data = json.loads(cached_price)
        last_updated = datetime.fromisoformat(data['timestamp'])
        now = datetime.utcnow()
        
        age_seconds = (now - last_updated).total_seconds()
        
        assert age_seconds < 300, f"Preço desatualizado: {age_seconds}s"
        print(f"✅ Preço atualizado há {age_seconds:.0f}s")
```

---

### 2.2 Validação de Sanidade (Z-score)

**Teste:**
```python
def test_price_sanity_check():
    """Testa rejeição de preços anômalos"""
    historical_prices = [180.0, 182.0, 185.0, 184.0, 183.0]  # Média ~182.8
    
    # Preço normal (dentro de 2 desvios)
    normal_price = 190.0
    assert sanity_check(normal_price, historical_prices) == True
    
    # Preço anômalo (>3 desvios)
    anomalous_price = 250.0
    assert sanity_check(anomalous_price, historical_prices) == False
    
    print("✅ Validação de sanidade funcionando")
```

---

### 2.3 Fallback entre Fontes

**Teste:**
```python
def test_price_fallback():
    """Testa fallback quando API principal falha"""
    # Simular falha da API CEPEA
    with patch('requests.get', side_effect=requests.RequestException()):
        price = fetch_soybean_price()
        
        # Deve usar fonte alternativa
        assert price is not None
        assert price['source'] != 'CEPEA/ESALQ'
        print("✅ Fallback funcionando")
```

---

### 2.4 Cache TTL

**Teste:**
```python
def test_cache_ttl():
    """Verifica que cache expira após 5 minutos"""
    redis_client = redis.from_url("redis://localhost:6379/0")
    
    # Inserir preço no cache
    redis_client.setex("price:test", 300, json.dumps({"price": 185.50}))
    
    # Verificar que existe
    assert redis_client.get("price:test") is not None
    
    # Aguardar 6 minutos
    time.sleep(360)
    
    # Verificar que expirou
    assert redis_client.get("price:test") is None
    print("✅ Cache TTL funcionando")
```

---

## 3. Testes de Upload

### 3.1 Validação de Schema

**Teste:**
```python
def test_upload_schema_validation():
    """Testa validação de schema no upload"""
    
    # CSV com colunas inválidas
    invalid_csv = """
    field_id,area,date
    1,45.2,2024-10-20
    """
    
    response = requests.post(
        'https://api.siad-agro.com/v1/upload/validate',
        files={'file': ('data.csv', invalid_csv)},
        data={'format': 'csv'}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['valid'] == False
    assert len(data['errors']) > 0
    print("✅ Validação de schema funcionando")
```

---

### 3.2 Mapeamento Automático de Colunas

**Teste:**
```python
def test_column_mapping():
    """Testa sugestão automática de mapeamento"""
    
    csv_content = """
    field_id,area_hectares,data_plantio,variedade,produtividade_kg_ha
    1,45.2,2024-10-20,BMX Potência,3450
    """
    
    response = requests.post(
        'https://api.siad-agro.com/v1/upload/validate',
        files={'file': ('data.csv', csv_content)},
        data={'format': 'csv'}
    )
    
    data = response.json()
    mapping = data['suggested_mapping']
    
    assert mapping['field_id'] == 'field_id'
    assert mapping['area_ha'] == 'area_hectares'
    assert mapping['planting_date'] == 'data_plantio'
    print("✅ Mapeamento automático funcionando")
```

---

### 3.3 Preview e Rollback

**Teste:**
```python
def test_upload_rollback():
    """Testa rollback em caso de erro"""
    
    # Fazer upload com dados inválidos
    response = requests.post(
        'https://api.siad-agro.com/v1/upload/ingest',
        json={
            'file_id': 'test-uuid',
            'column_mapping': {...},
            'options': {'create_fields': True}
        }
    )
    
    job_id = response.json()['job_id']
    
    # Aguardar conclusão
    status = wait_for_job_completion(job_id)
    
    if status['status'] == 'failed':
        # Verificar que rollback foi feito
        assert count_fields_in_db() == initial_count
        print("✅ Rollback funcionando")
```

---

## 4. Testes de Exportação

### 4.1 Geração de PDF

**Teste:**
```python
def test_pdf_generation():
    """Testa geração de relatório PDF"""
    
    response = requests.post(
        'https://api.siad-agro.com/v1/reports/generate',
        json={
            'template': 'summary',
            'fields': [1, 3, 4],
            'format': 'pdf',
            'options': {'include_map': True, 'watermark': True}
        }
    )
    
    report_id = response.json()['report_id']
    
    # Aguardar geração
    time.sleep(45)
    
    # Download
    pdf_response = requests.get(
        f'https://api.siad-agro.com/v1/reports/{report_id}/download'
    )
    
    assert pdf_response.status_code == 200
    assert pdf_response.headers['Content-Type'] == 'application/pdf'
    
    # Validar tamanho (deve ter conteúdo)
    assert len(pdf_response.content) > 10000  # > 10KB
    
    print("✅ Geração de PDF funcionando")
```

---

### 4.2 Exportação GeoJSON

**Teste:**
```python
def test_geojson_export():
    """Testa exportação em formato GeoJSON"""
    
    response = requests.get(
        'https://api.siad-agro.com/v1/map/fields',
        params={'farm_id': 1, 'format': 'geojson'}
    )
    
    assert response.status_code == 200
    geojson = response.json()
    
    # Validar estrutura GeoJSON
    assert geojson['type'] == 'FeatureCollection'
    assert 'features' in geojson
    assert len(geojson['features']) > 0
    
    # Validar geometria
    feature = geojson['features'][0]
    assert 'geometry' in feature
    assert 'properties' in feature
    
    print("✅ Exportação GeoJSON funcionando")
```

---

## 5. Testes de Simulação What-If

### 5.1 Latência < 2s

**Teste:**
```python
def test_simulation_latency():
    """Testa que simulação responde em < 2s"""
    
    start = time.time()
    
    response = requests.post(
        'https://api.siad-agro.com/v1/simulations/what-if',
        json={
            'field_id': 1,
            'scenario': {
                'rainfall_mm': 850,
                'soybean_price_r_sc': 170.0,
                'fertilizer_n_kg_ha': 80
            }
        }
    )
    
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 2.0, f"Latência excedida: {elapsed:.2f}s"
    
    print(f"✅ Simulação concluída em {elapsed:.2f}s")
```

---

### 5.2 Explicabilidade (SHAP)

**Teste:**
```python
def test_shap_explainability():
    """Testa que simulação retorna valores SHAP"""
    
    response = requests.post(
        'https://api.siad-agro.com/v1/simulations/what-if',
        json={...}
    )
    
    data = response.json()
    
    assert 'explainability' in data
    assert 'shap_values' in data['explainability']
    
    shap = data['explainability']['shap_values']
    assert 'rainfall' in shap
    assert 'price' in shap
    
    print("✅ Explicabilidade funcionando")
```

---

## 6. Testes de Tolerância a Falhas

### 6.1 Disponibilidade de APIs Externas

**Teste:**
```python
def test_api_resilience():
    """Testa comportamento quando APIs externas falham"""
    
    # Simular falha da API de preços
    with patch('requests.get', side_effect=requests.RequestException()):
        response = requests.get('https://api.siad-agro.com/v1/prices/current')
        
        # Deve retornar último valor em cache ou erro 503
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert 'cache_ttl_seconds' in data['soybean']['spot']
            print("✅ Fallback para cache funcionando")
```

---

### 6.2 Consistência de Dados

**Teste:**
```python
def test_data_consistency():
    """Testa consistência após falhas"""
    
    # Fazer upload
    upload_response = requests.post(...)
    job_id = upload_response.json()['job_id']
    
    # Simular falha durante processamento
    # (kill processo, reiniciar)
    
    # Verificar que dados não foram parcialmente inseridos
    assert count_partial_records() == 0
    
    # Verificar que job pode ser retomado
    status = requests.get(f'/upload/status/{job_id}').json()
    assert status['status'] in ['processing', 'failed', 'completed']
    
    print("✅ Consistência de dados mantida")
```

---

## 7. Critérios de Aceitação

### 7.1 Performance

| Métrica | Target | Medição |
|---------|--------|---------|
| Latência p95 (APIs) | < 500ms | k6, Locust |
| Throughput | 1000 req/s | Load test |
| Upload (10k linhas) | < 30s | Teste manual |
| Simulação What-If | < 2s | Teste automatizado |
| Geração PDF | < 45s | Teste automatizado |

### 7.2 Disponibilidade

| Métrica | Target |
|---------|--------|
| Uptime | 99.9% (8.76h downtime/ano) |
| MTTR (Mean Time To Repair) | < 1 hora |
| RPO (Recovery Point Objective) | < 5 minutos |

### 7.3 Precisão

| Métrica | Target |
|---------|--------|
| Preços atualizados | A cada 5 min ± 30s |
| Validação de preços (z-score) | Rejeitar > 3 desvios |
| NDVI cálculo | Erro < 0.01 |

### 7.4 Segurança

| Métrica | Target |
|---------|--------|
| Autenticação | OAuth2 + JWT |
| Rate limiting | 100 req/min por usuário |
| TLS | TLS 1.3 obrigatório |
| Logs | Estruturados, sem dados sensíveis |

---

## 8. Ambiente de Testes

### 8.1 Staging

- Banco de dados: PostgreSQL + PostGIS (dados sintéticos)
- Cache: Redis (TTL reduzido para testes)
- APIs externas: Mock servers (WireMock)

### 8.2 CI/CD

- Testes unitários: pytest, jest
- Testes de integração: Docker Compose
- Testes E2E: Cypress, Playwright
- Testes de performance: k6 (GitHub Actions)

---

## 9. Monitoramento

### 9.1 Métricas

- Prometheus + Grafana
- APM: New Relic / Datadog
- Logs: ELK Stack

### 9.2 Alertas

- Latência p95 > 500ms
- Taxa de erro > 1%
- Preços não atualizados > 10 min
- CPU > 80%
- Memória > 80%


