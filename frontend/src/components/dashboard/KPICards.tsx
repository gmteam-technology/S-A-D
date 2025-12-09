"use client"

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Map, TrendingUp, Droplets, Dna, DollarSign, FileText } from 'lucide-react'
import { api } from '@/lib/api'

interface KPIData {
  area_ha: number
  avg_productivity_kg_ha: number
  total_yield_t: number
  avg_moisture_pct: number
  avg_protein_pct: number
  estimated_margin_r_ha: number
  last_updated: string
}

const kpiConfig = [
  {
    key: 'area_ha',
    label: 'Área Plantada',
    icon: Map,
    unit: 'ha',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 1 }),
    color: 'text-blue-600 dark:text-blue-400',
    bgColor: 'bg-blue-50 dark:bg-blue-500/10',
    action: 'Ver Mapa'
  },
  {
    key: 'avg_productivity_kg_ha',
    label: 'Produtividade Média',
    icon: TrendingUp,
    unit: 'kg/ha',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 0 }),
    color: 'text-emerald-600 dark:text-emerald-400',
    bgColor: 'bg-emerald-50 dark:bg-emerald-500/10',
    action: 'Ver Detalhes'
  },
  {
    key: 'total_yield_t',
    label: 'Rendimento Total',
    icon: FileText,
    unit: 't',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 1 }),
    color: 'text-amber-600 dark:text-amber-400',
    bgColor: 'bg-amber-50 dark:bg-amber-500/10',
    action: 'Gerar PDF'
  },
  {
    key: 'avg_moisture_pct',
    label: 'Umidade Média',
    icon: Droplets,
    unit: '%',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 1 }),
    color: 'text-cyan-600 dark:text-cyan-400',
    bgColor: 'bg-cyan-50 dark:bg-cyan-500/10',
    action: 'Ver Histórico'
  },
  {
    key: 'avg_protein_pct',
    label: 'Proteína',
    icon: Dna,
    unit: '%',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 1 }),
    color: 'text-purple-600 dark:text-purple-400',
    bgColor: 'bg-purple-50 dark:bg-purple-500/10',
    action: 'Ver Análise'
  },
  {
    key: 'estimated_margin_r_ha',
    label: 'Margem Estimada',
    icon: DollarSign,
    unit: 'R$/ha',
    format: (val: number) => val.toLocaleString('pt-BR', { maximumFractionDigits: 0 }),
    color: 'text-green-600 dark:text-green-400',
    bgColor: 'bg-green-50 dark:bg-green-500/10',
    action: 'Simular'
  }
]

export function KPICards() {
  const { data: kpis, isLoading } = useQuery<KPIData>({
    queryKey: ['dashboard', 'kpis'],
    queryFn: api.getKPIs,
    refetchInterval: 30000 // Atualizar a cada 30s
  })

  if (isLoading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        {kpiConfig.map((kpi) => (
          <div key={kpi.key} className="h-32 animate-pulse rounded-2xl bg-slate-200 dark:bg-slate-800" />
        ))}
      </div>
    )
  }

  if (!kpis) return null

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
      {kpiConfig.map((config) => {
        const Icon = config.icon
        const value = kpis[config.key as keyof KPIData] as number

        if (!Icon) {
          console.error(`Icon not found for KPI: ${config.key}`)
          return null
        }

        return (
          <motion.div
            key={config.key}
            className={`group relative overflow-hidden rounded-2xl border border-slate-100 ${config.bgColor} p-4 shadow-card transition-all hover:shadow-lg dark:border-slate-800`}
            whileHover={{ y: -4, scale: 1.02 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-xs font-medium uppercase tracking-wide text-slate-600 dark:text-slate-400">
                  {config.label}
                </p>
                <div className="mt-2 flex items-baseline gap-2">
                  <p className={`text-2xl font-bold ${config.color}`}>
                    {config.format(value)}
                  </p>
                  <span className="text-sm text-slate-500">{config.unit}</span>
                </div>
              </div>
              <div className={`rounded-lg ${config.bgColor} p-2`}>
                <Icon className={`h-5 w-5 ${config.color}`} />
              </div>
            </div>
            <button className="mt-3 w-full rounded-lg bg-white/60 px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-white/80 dark:bg-slate-800/60 dark:text-slate-300 dark:hover:bg-slate-800/80">
              {config.action}
            </button>
          </motion.div>
        )
      })}
    </div>
  )
}


