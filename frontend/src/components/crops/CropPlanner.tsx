"use client"

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { CropSeason } from '@/lib/types'
import { motion } from 'framer-motion'

export function CropPlanner() {
  const { data: seasons = [] } = useQuery<CropSeason[]>({ queryKey: ['seasons'], queryFn: api.seasons })

  return (
    <section className="mt-10 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Módulo de safras</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-900 dark:text-white">Planejamento de plantio & colheita</h2>
        </div>
        <button className="rounded-full border border-slate-200 px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-white dark:border-slate-700 dark:text-slate-200">Adicionar safra</button>
      </div>
      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="pb-3">Safra</th>
              <th>Área (ha)</th>
              <th>Produtividade</th>
              <th>Custo/ha</th>
              <th>Margem</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {seasons.map((season) => (
              <tr key={season.name} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">
                <td className="py-3 font-semibold text-slate-900 dark:text-white">{season.name}</td>
                <td>{season.area.toLocaleString('pt-BR')}</td>
                <td>{season.productivity} sc/ha</td>
                <td>R$ {season.costPerHa.toLocaleString('pt-BR')}</td>
                <td className="text-emerald-500">R$ {season.margin.toLocaleString('pt-BR')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
