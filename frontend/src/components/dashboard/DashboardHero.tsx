"use client"

import { motion } from 'framer-motion'
import { useLocale } from '@/contexts/locale-context'

export function DashboardHero() {
  const { t } = useLocale()
  return (
    <section className="mb-10 grid gap-6 rounded-3xl border border-white/60 bg-white/70 p-6 shadow-card backdrop-blur supports-[backdrop-filter]:bg-white/70 dark:border-slate-800/80 dark:bg-slate-900/60">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Resumo das safras</p>
        <div className="mt-2 flex flex-wrap items-baseline gap-3">
          <h2 className="text-3xl font-semibold text-slate-900 dark:text-white">{t('heroTitle')}</h2>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-300">
            IA + Simulações em tempo real
          </span>
        </div>
        <p className="mt-3 max-w-2xl text-base text-slate-600 dark:text-slate-300">{t('heroSubtitle')}</p>
      </motion.div>
      <div className="grid gap-4 sm:grid-cols-4">
        {[
          { label: 'Talhões monitorados', value: '48', detail: '+6 vs última safra' },
          { label: 'NDVI médio', value: '0,72', detail: 'Zona verde saudável' },
          { label: 'Margem projetada', value: 'R$ 58,4 mi', detail: '+4,2% semanal' },
          { label: 'Alertas críticos', value: '3', detail: '2 clima · 1 praga' },
        ].map((item) => (
          <motion.div
            key={item.label}
            className="rounded-2xl border border-slate-100 bg-white/80 p-4 shadow-card dark:border-slate-800 dark:bg-slate-900/70"
            whileHover={{ y: -4 }}
          >
            <p className="text-xs uppercase tracking-wide text-slate-500">{item.label}</p>
            <p className="mt-2 text-2xl font-semibold text-slate-900 dark:text-white">{item.value}</p>
            <p className="text-sm text-emerald-500 dark:text-emerald-300">{item.detail}</p>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
