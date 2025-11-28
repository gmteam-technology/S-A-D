export type EconomicIndicator = {
  label: string
  value: string
  trend: 'up' | 'down' | 'flat'
  delta: string
}

export type WeatherDay = {
  date: string
  min: number
  max: number
  rainfall: number
  risk: number
}

export type CropSeason = {
  name: string
  area: number
  productivity: number
  costPerHa: number
  margin: number
}

export type ScenarioConfig = {
  id: string
  title: string
  rainfallDelta: number
  inputDelta: number
  fertilizationDelta: number
  cultivar: string
  price: number
}

export type FieldLayer = {
  id: string
  label: string
  active: boolean
}

export type RainChartPoint = {
  day: string
  rainfall: number
  eto: number
}
