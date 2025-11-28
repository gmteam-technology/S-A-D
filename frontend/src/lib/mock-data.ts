import { CropSeason, EconomicIndicator, RainChartPoint, ScenarioConfig, WeatherDay } from './types'

export const weatherMock: WeatherDay[] = [
  { date: '2025-11-28', min: 19, max: 32, rainfall: 8, risk: 0.2 },
  { date: '2025-11-29', min: 20, max: 31, rainfall: 18, risk: 0.4 },
  { date: '2025-11-30', min: 21, max: 33, rainfall: 12, risk: 0.35 },
  { date: '2025-12-01', min: 22, max: 34, rainfall: 5, risk: 0.15 },
  { date: '2025-12-02', min: 21, max: 35, rainfall: 14, risk: 0.5 },
  { date: '2025-12-03', min: 20, max: 32, rainfall: 9, risk: 0.24 },
  { date: '2025-12-04', min: 19, max: 30, rainfall: 16, risk: 0.42 },
]

export const econMock: EconomicIndicator[] = [
  { label: 'Custo/ha', value: 'R$ 4.180', trend: 'up', delta: '+3.1%' },
  { label: 'Margem esperada', value: 'R$ 2.430', trend: 'up', delta: '+5.4%' },
  { label: 'Preço saca', value: 'R$ 152,00', trend: 'flat', delta: '+0.2%' },
  { label: 'Insumos', value: 'R$ 2.980', trend: 'down', delta: '-1.2%' },
]

export const rainChartMock: RainChartPoint[] = [
  { day: 'Seg', rainfall: 12, eto: 4.1 },
  { day: 'Ter', rainfall: 4, eto: 3.8 },
  { day: 'Qua', rainfall: 22, eto: 4.6 },
  { day: 'Qui', rainfall: 16, eto: 4.0 },
  { day: 'Sex', rainfall: 9, eto: 3.9 },
  { day: 'Sáb', rainfall: 3, eto: 3.6 },
  { day: 'Dom', rainfall: 18, eto: 4.4 },
]

export const seasonsMock: CropSeason[] = [
  { name: 'Safra 23/24', area: 3200, productivity: 61.5, costPerHa: 4120, margin: 2480 },
  { name: 'Safra 22/23', area: 2950, productivity: 58.2, costPerHa: 3980, margin: 2310 },
  { name: 'Safrinha 23', area: 1800, productivity: 92.3, costPerHa: 2870, margin: 1840 },
]

export const scenariosMock: ScenarioConfig[] = [
  { id: 'base', title: 'Baseline', rainfallDelta: 0, inputDelta: 0, fertilizationDelta: 0, cultivar: 'SOJA RR', price: 152 },
  { id: 'rain+', title: '+10% chuva', rainfallDelta: 10, inputDelta: 0, fertilizationDelta: 3, cultivar: 'SOJA IPRO', price: 158 },
  { id: 'insumos-', title: '-8% insumos', rainfallDelta: 0, inputDelta: -8, fertilizationDelta: 0, cultivar: 'SOJA RR', price: 150 },
]
