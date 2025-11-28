"use client"

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { useMemo, useState } from 'react'
import { api } from '@/lib/api'
import { ScenarioConfig } from '@/lib/types'

const sliders = [
  { id: 'rain', label: 'Variação de chuva', suffix: '%', min: -20, max: 20 },
  { id: 'inputs', label: 'Variação insumos', suffix: '%', min: -20, max: 20 },
  { id: 'fert', label: 'Ajuste adubação', suffix: '%', min: -10, max: 10 },
]

export function ScenarioSimulator() {
  const { data: scenarios = [] } = useQuery<ScenarioConfig[]>({ queryKey: ['scenarios'], queryFn: api.scenarios })
  const [config, setConfig] = useState({ rain: 10, inputs: -5, fert: 3, price: 152 })

  const result = useMemo(() => {
    const yieldBase = 58
    const marginBase = 2400
    const projectedYield = yieldBase * (1 + config.rain / 100) * (1 + config.fert / 200)
    const projectedCost = 4100 * (1 + config.inputs / 100)
    const projectedMargin = projectedYield * config.price - projectedCost
    return {
      projectedYield: projectedYield.toFixed(1),
      projectedMargin: `R$ ${(projectedMargin / 1000).toFixed(1)}k`,
      risk: Math.max(0.2, 1 - Math.abs(config.rain) / 100 - Math.abs(config.inputs) / 120).toFixed(2),
    }
  }, [config])

  return (
    <section className="mt-10 grid gap-6 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Cenários agrícolas</p>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Simulações what-if em tempo real</h2>
        </div>
        <div className="flex flex-wrap gap-3">
          {['chuva', 'insumos', 'cultivar', 'preço'].map((pill) => (
            <span key={pill} className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">
              {pill}
            </span>
          ))}
        </div>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-6">
          {sliders.map((slider) => (
            <div key={slider.id}>
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-slate-600">{slider.label}</p>
                <span className="text-sm font-semibold text-slate-900 dark:text-slate-100">{config[slider.id as keyof typeof config]}{slider.suffix}</span>
              </div>
              <input
                type="range"
                min={slider.min}
                max={slider.max}
                value={config[slider.id as keyof typeof config]}
                onChange={(event) => setConfig((prev) => ({ ...prev, [slider.id]: Number(event.target.value) }))}
                className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-200 accent-brand-500"
              />
            </div>
          ))}
          <label className="text-sm font-medium text-slate-600">Preço da saca (R$)
            <input
              type="number"
              value={config.price}
              onChange={(event) => setConfig((prev) => ({ ...prev, price: Number(event.target.value) }))}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-white/70 px-3 py-2 text-slate-900 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>
        </div>
        <div className="space-y-4">
          <motion.div className="rounded-3xl border border-brand-100 bg-gradient-to-br from-brand-500 to-indigo-600 p-6 text-white shadow-2xl" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-sm uppercase tracking-[0.5em] text-white/70">Resultado simulado</p>
            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              <div>
                <p className="text-sm text-white/80">Produtividade</p>
                <p className="text-3xl font-semibold">{result.projectedYield} sc/ha</p>
              </div>
              <div>
                <p className="text-sm text-white/80">Margem</p>
                <p className="text-3xl font-semibold">{result.projectedMargin}</p>
              </div>
              <div>
                <p className="text-sm text-white/80">Risco</p>
                <p className="text-3xl font-semibold">{result.risk}</p>
              </div>
            </div>
          </motion.div>
          <div className="grid gap-4 sm:grid-cols-3">
            {scenarios.map((scenario) => (
              <motion.div key={scenario.id} whileHover={{ y: -4, scale: 1.01 }} className="rounded-2xl border border-slate-200 bg-white/80 p-4 dark:border-slate-800 dark:bg-slate-900/70">
                <p className="text-xs uppercase text-slate-500">{scenario.title}</p>
                <p className="mt-2 text-lg font-semibold text-slate-900 dark:text-white">{scenario.cultivar}</p>
                <p className="text-sm text-emerald-500">Preço R$ {scenario.price}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
