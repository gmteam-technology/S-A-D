"use client"

import { motion } from 'framer-motion'
import Image from 'next/image'

const indicators = [
  { label: 'ETo', value: '4,2 mm', status: 'Estável' },
  { label: 'NDVI', value: '0,72', status: 'Alta vigor' },
  { label: 'Kc', value: '0,95', status: 'CD stage' },
]

export function ClimatologyPanel() {
  return (
    <section className="mt-10 grid gap-6 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70 lg:grid-cols-3">
      <div className="lg:col-span-2">
        <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Módulo climatológico</p>
        <h2 className="mt-2 text-2xl font-semibold text-slate-900 dark:text-white">Previsão + Histórico por talhão</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {indicators.map((indicator) => (
            <motion.div key={indicator.label} className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4 shadow-card dark:border-slate-800 dark:bg-slate-900/60" whileHover={{ y: -4 }}>
              <p className="text-xs uppercase tracking-wide text-slate-500">{indicator.label}</p>
              <p className="mt-2 text-2xl font-semibold text-slate-900 dark:text-white">{indicator.value}</p>
              <p className="text-sm text-emerald-500">{indicator.status}</p>
            </motion.div>
          ))}
        </div>
        <div className="mt-6 rounded-2xl border border-slate-100 bg-gradient-to-r from-slate-900 to-slate-800 p-5 text-white shadow-card">
          <p className="text-xs uppercase tracking-[0.5em] text-white/60">Radar meteorológico</p>
          <p className="mt-2 text-lg font-semibold">Células de chuva entrando pelo Oeste em 32 min</p>
          <p className="text-sm text-white/70">Integração com INMET + Sentinel | atualização a cada 5 min</p>
        </div>
      </div>
      <motion.div className="rounded-2xl border border-slate-100 bg-slate-50/60 p-4 dark:border-slate-800 dark:bg-slate-900/60" initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }}>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Radar ao vivo</p>
        <div className="mt-4 h-80 w-full rounded-2xl bg-gradient-to-br from-slate-100 to-white dark:from-slate-800 dark:to-slate-900">
          <Image src="/globe.svg" alt="Radar" width={320} height={320} className="h-full w-full object-contain p-6 opacity-80" />
        </div>
      </motion.div>
    </section>
  )
}
