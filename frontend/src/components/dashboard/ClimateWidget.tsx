"use client"

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { api } from '@/lib/api'
import { WeatherDay } from '@/lib/types'
import { Droplets, Wind } from 'lucide-react'

export function ClimateWidget() {
  const { data: days = [] } = useQuery({ queryKey: ['forecast'], queryFn: api.weatherForecast })

  return (
    <motion.div layout data-testid="widget-clima" className="h-full rounded-2xl border border-white/70 bg-white/80 p-4 shadow-card dark:border-slate-800 dark:bg-slate-900/70" whileHover={{ y: -4 }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">Previsão 7 dias</p>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Clima & risco climático</h3>
        </div>
        <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-500/10 dark:text-blue-200">Radar ativo</span>
      </div>
      <div className="mt-4 space-y-3">
        {days.map((day) => (
          <div key={day.date} className="flex items-center justify-between rounded-xl border border-slate-100 px-3 py-2 text-sm dark:border-slate-800">
            <div>
              <p className="font-medium text-slate-900 dark:text-white">{new Date(day.date).toLocaleDateString('pt-BR', { weekday: 'short', day: '2-digit', month: '2-digit' })}</p>
              <p className="text-xs text-slate-500">Risco {(day.risk * 100).toFixed(0)}%</p>
            </div>
            <div className="flex items-center gap-4 text-slate-600 dark:text-slate-200">
              <span>{day.min}º / {day.max}º</span>
              <div className="flex items-center gap-1 text-blue-500"><Droplets className="h-4 w-4" />{day.rainfall}mm</div>
              <div className="flex items-center gap-1 text-amber-500"><Wind className="h-4 w-4" />{Math.round(day.risk * 10)}km/h</div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
