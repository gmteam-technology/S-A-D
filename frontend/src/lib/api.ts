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
}
