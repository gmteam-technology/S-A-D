"use client"

import { useQuery } from '@tanstack/react-query'
import { Area, AreaChart, CartesianGrid, Tooltip, XAxis, YAxis, ResponsiveContainer, Line } from 'recharts'
import { api } from '@/lib/api'
import { RainChartPoint } from '@/lib/types'
import { motion } from 'framer-motion'

export function RainfallWidget() {
  const { data: series = [] } = useQuery<RainChartPoint[]>({ queryKey: ['rain'], queryFn: api.rainChart })

  return (
    <motion.div layout className="rounded-2xl border border-white/70 bg-white/80 p-4 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">Chuvas x ETo</p>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Talhão Rio Verde</h3>
        </div>
        <span className="text-xs font-medium text-slate-500">Últimos 7 dias</span>
      </div>
      <div className="h-56 min-h-[224px] pt-4">
        <ResponsiveContainer width="100%" height="100%" minHeight={200}>
          <AreaChart data={series} margin={{ top: 10, left: 0, right: 0 }}>
            <defs>
              <linearGradient id="rain" x1="0" x2="0" y1="0" y2="1">
                <stop offset="5%" stopColor="#2f6afe" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#2f6afe" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="day" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" yAxisId="left" />
            <YAxis orientation="right" yAxisId="right" stroke="#94a3b8" hide />
            <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #e2e8f0' }} />
            <Area type="monotone" dataKey="rainfall" stroke="#2f6afe" fill="url(#rain)" yAxisId="left" />
            <Line type="monotone" dataKey="eto" stroke="#f59e0b" strokeWidth={2} dot={false} yAxisId="right" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  )
}
