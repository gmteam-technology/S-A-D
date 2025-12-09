import { econMock, rainChartMock, scenariosMock, seasonsMock, weatherMock } from './mock-data'
import { CropSeason, EconomicIndicator, ScenarioConfig, WeatherDay } from './types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

type FetchArgs<T> = {
  path: string
  fallback: T
}

async function request<T>({ path, fallback }: FetchArgs<T>): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, { next: { revalidate: 60 } })
    if (!response.ok) throw new Error('Falha ao consultar API')
    return (await response.json()) as T
  } catch (error) {
    console.warn(`[API fallback] ${path}`, error)
    return fallback
  }
}

export const api = {
  weatherForecast: async () => {
    const data = await request<{ forecast: WeatherDay[] }>({
      path: '/weather/forecast?station=BR001',
      fallback: { forecast: weatherMock },
    })
    return data.forecast ?? weatherMock
  },
  economicIndicators: async () => {
    const data = await request<{ yield_bag_ha: number; cost_per_ha: number; efficiency_index: number }[]>({
      path: '/crops/productivity?season_id=1',
      fallback: [],
    })
    if (!data.length) return econMock
    return [
      { label: 'Custo/ha', value: `R$ ${data[0].cost_per_ha.toLocaleString('pt-BR')}`, trend: 'up', delta: '+3.1%' },
      { label: 'Produtividade', value: `${data[0].yield_bag_ha.toFixed(1)} sc/ha`, trend: 'flat', delta: '+0.4%' },
      { label: 'Eficiência', value: data[0].efficiency_index.toFixed(2), trend: 'up', delta: '+1.1%' },
      { label: 'Margem', value: 'R$ 2.430', trend: 'up', delta: '+5.4%' },
    ] satisfies EconomicIndicator[]
  },
  rainChart: async () => {
    const data = await request<{ history: { rainfall_mm: number; eto: number; reading_date?: string }[] }>({
      path: '/weather/history?station=BR001',
      fallback: { history: [] },
    })
    if (!data.history?.length) return rainChartMock
    return data.history.slice(0, 7).map((row, idx) => ({
      day: row.reading_date ? new Date(row.reading_date).toLocaleDateString('pt-BR', { weekday: 'short' }) : `Dia ${idx + 1}`,
      rainfall: row.rainfall_mm,
      eto: row.eto,
    }))
  },
  seasons: () => request<CropSeason[]>({ path: '/crops/season', fallback: seasonsMock }),
  scenarios: () => Promise.resolve(scenariosMock as ScenarioConfig[]),
  getKPIs: async () => {
    const data = await request<{
      area_ha: number
      avg_productivity_kg_ha: number
      total_yield_t: number
      avg_moisture_pct: number
      avg_protein_pct: number
      estimated_margin_r_ha: number
      last_updated: string
    }>({
      path: '/dashboard/kpis',
      fallback: {
        area_ha: 1250.5,
        avg_productivity_kg_ha: 3450.2,
        total_yield_t: 4312.8,
        avg_moisture_pct: 13.2,
        avg_protein_pct: 38.5,
        estimated_margin_r_ha: 2100.0,
        last_updated: new Date().toISOString()
      }
    })
    return data
  },
  getCurrentPrices: async () => {
    const data = await request<{
      soybean: {
        spot: {
          price_r_sc: number
          price_r_t: number
          source: string
          timestamp: string
          last_updated: string
          cache_ttl_seconds: number
        }
        contract: {
          price_r_sc: number
          maturity: string
          source: string
          timestamp: string
        }
      }
      fertilizer: {
        npk_10_10_10: {
          price_r_t: number
          source: string
          timestamp: string
        }
      }
      freight: {
        price_r_t: number
        route: string
        distance_km: number
        source: string
        timestamp: string
      }
    }>({
      path: '/prices/current',
      fallback: {
        soybean: {
          spot: {
            price_r_sc: 185.50,
            price_r_t: 3108.33,
            source: 'CEPEA/ESALQ',
            timestamp: new Date().toISOString(),
            last_updated: new Date().toISOString(),
            cache_ttl_seconds: 300
          },
          contract: {
            price_r_sc: 188.20,
            maturity: '2025-03',
            source: 'B3',
            timestamp: new Date().toISOString()
          }
        },
        fertilizer: {
          npk_10_10_10: {
            price_r_t: 3450.00,
            source: 'ANDA',
            timestamp: new Date().toISOString()
          }
        },
        freight: {
          price_r_t: 85.00,
          route: 'Fazenda → Port',
          distance_km: 120,
          source: 'AgroFreight API',
          timestamp: new Date().toISOString()
        }
      }
    })
    return data
  },
}
