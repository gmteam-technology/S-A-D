"use client"

import { useQuery } from '@tanstack/react-query'
import { TrendingDown, TrendingUp, Minus } from 'lucide-react'
import { api } from '@/lib/api'
import { EconomicIndicator } from '@/lib/types'
import { motion } from 'framer-motion'

const iconMap = {
  up: TrendingUp,
  down: TrendingDown,
  flat: Minus,
}

export function EconomicWidget() {
  const { data: indicators = [] } = useQuery<EconomicIndicator[]>({ queryKey: ['economics'], queryFn: api.economicIndicators })

  return (
    <motion.div data-testid="widget-economia" layout className="rounded-2xl border border-white/70 bg-gradient-to-br from-brand-500/10 via-white to-white p-5 shadow-card dark:border-slate-800 dark:from-brand-500/10 dark:via-slate-900 dark:to-slate-900">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">Indicadores econômicos</p>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Sensibilidade financeiro</h3>
        </div>
        <span className="rounded-full bg-brand-500 px-3 py-1 text-xs font-semibold text-white">Atualizado 5 min</span>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {indicators.map((indicator) => {
          const Icon = iconMap[indicator.trend]
          const trendColor = indicator.trend === 'up' ? 'text-emerald-500' : indicator.trend === 'down' ? 'text-rose-500' : 'text-slate-500'
          return (
            <div key={indicator.label} className="rounded-xl border border-white/60 bg-white/70 p-4 shadow-card dark:border-slate-800 dark:bg-slate-900/60">
              <p className="text-xs uppercase tracking-wide text-slate-500">{indicator.label}</p>
              <div className="mt-2 flex items-center justify-between">
                <p className="text-2xl font-semibold text-slate-900 dark:text-white">{indicator.value}</p>
                <span className={`flex items-center gap-1 text-sm font-semibold ${trendColor}`}>
                  <Icon className="h-4 w-4" />
                  {indicator.delta}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </motion.div>
  )
}
