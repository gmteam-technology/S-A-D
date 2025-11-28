"use client"

import { motion } from 'framer-motion'
import { FileText, Download, Share2 } from 'lucide-react'

const reports = [
  { title: 'Relatório de Safra', type: 'PDF', status: 'Pronto', color: 'from-emerald-500 to-teal-500' },
  { title: 'Tendência de chuva', type: 'CSV', status: 'Gerando', color: 'from-sky-500 to-blue-500' },
  { title: 'Mapa com camadas', type: 'PDF', status: 'Pronto', color: 'from-amber-500 to-orange-500' },
]

export function ReportCenter() {
  return (
    <section className="mt-10 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Relatórios & exportações</p>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">PDF, CSV e camadas em poucos cliques</h2>
        </div>
        <button className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow dark:bg-white dark:text-slate-900">
          <Share2 className="h-4 w-4" />Compartilhar link seguro
        </button>
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {reports.map((report) => (
          <motion.div key={report.title} whileHover={{ y: -4 }} className={`rounded-2xl border border-white/60 bg-gradient-to-br ${report.color} p-4 text-white shadow-card`}>
            <p className="text-xs uppercase tracking-[0.3em] text-white/70">{report.type}</p>
            <p className="mt-2 text-xl font-semibold">{report.title}</p>
            <p className="text-sm text-white/80">Status: {report.status}</p>
            <div className="mt-4 flex gap-2 text-sm">
              <button className="inline-flex flex-1 items-center justify-center gap-2 rounded-full bg-white/20 py-2 font-semibold text-white">
                <FileText className="h-4 w-4" />Abrir
              </button>
              <button className="rounded-full bg-white/20 p-2 text-white">
                <Download className="h-4 w-4" />
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
