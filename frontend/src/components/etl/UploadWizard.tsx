"use client"

import { useState } from 'react'
import { motion } from 'framer-motion'

const steps = [
  { title: 'Upload CSV/XLSX', description: 'Arraste arquivos de produtividade, chuva ou custos.' },
  { title: 'Limpeza automática', description: 'Normalizamos colunas, unidades e coordenadas.' },
  { title: 'Mapeamento', description: 'Ajuste colunas (chuva, NDVI, solo) antes de enviar.' },
  { title: 'Validação Geo', description: 'Validamos poligonais GeoJSON com PostGIS.' },
]

export function UploadWizard() {
  const [selected, setSelected] = useState(0)
  const [fileName, setFileName] = useState<string | null>(null)

  return (
    <section className="mt-10 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">ETL agrícola</p>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Upload inteligente de dados</h2>
        </div>
        <button className="rounded-full bg-brand-500 px-5 py-2 text-sm font-semibold text-white shadow hover:-translate-y-0.5">Exportar relatório</button>
      </div>
      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-dashed border-brand-300 bg-brand-50/50 p-6 text-center dark:border-brand-500/40 dark:bg-brand-500/10">
          <p className="text-sm text-slate-600 dark:text-slate-200">Arraste arquivos CSV, XLSX, JSON ou GeoTIFF</p>
          <label className="mt-4 inline-flex cursor-pointer flex-col items-center gap-2 rounded-2xl bg-white/80 px-6 py-4 text-brand-600 shadow-card dark:bg-slate-900/70">
            <span className="text-sm font-medium">Selecionar arquivo</span>
            <input type="file" className="hidden" onChange={(event) => setFileName(event.target.files?.[0]?.name ?? null)} />
          </label>
          {fileName && <p className="mt-3 text-sm text-slate-500">Pronto para enviar: {fileName}</p>}
        </div>
        <div className="space-y-4">
          {steps.map((step, index) => (
            <motion.button
              key={step.title}
              onClick={() => setSelected(index)}
              className={`w-full rounded-2xl border px-4 py-3 text-left transition ${
                selected === index
                  ? 'border-brand-500 bg-brand-50/70 text-brand-700 shadow-card dark:border-brand-400 dark:bg-brand-500/10 dark:text-brand-200'
                  : 'border-slate-200 bg-white/70 text-slate-600 dark:border-slate-700 dark:bg-slate-900/70'
              }`}
            >
              <p className="text-sm font-semibold">{index + 1}. {step.title}</p>
              <p className="text-xs">{step.description}</p>
            </motion.button>
          ))}
        </div>
      </div>
    </section>
  )
}
