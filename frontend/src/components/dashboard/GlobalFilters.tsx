"use client"

import { useState, useEffect, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { MapPin, Calendar } from 'lucide-react'

interface FilterState {
  farm_id: string
  field_id: string
  variety: string
  season: string
  date_from: string
  date_to: string
}

function GlobalFiltersContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  const [filters, setFilters] = useState<FilterState>({
    farm_id: searchParams.get('farm_id') || '',
    field_id: searchParams.get('field_id') || '',
    variety: searchParams.get('variety') || '',
    season: searchParams.get('season') || '',
    date_from: searchParams.get('date_from') || '',
    date_to: searchParams.get('date_to') || ''
  })

  // Persistir no localStorage
  useEffect(() => {
    localStorage.setItem('dashboard_filters', JSON.stringify(filters))
  }, [filters])

  // Carregar do localStorage na inicialização
  useEffect(() => {
    const saved = localStorage.getItem('dashboard_filters')
    if (saved) {
      const parsed = JSON.parse(saved)
      setFilters(parsed)
    }
  }, [])

  const updateFilter = (key: keyof FilterState, value: string) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    
    // Atualizar URL params
    const params = new URLSearchParams()
    Object.entries(newFilters).forEach(([k, v]) => {
      if (v) params.set(k, v)
    })
    router.push(`?${params.toString()}`, { scroll: false })
  }

  const clearFilters = () => {
    const emptyFilters: FilterState = {
      farm_id: '',
      field_id: '',
      variety: '',
      season: '',
      date_from: '',
      date_to: ''
    }
    setFilters(emptyFilters)
    router.push('?', { scroll: false })
    localStorage.removeItem('dashboard_filters')
  }

  return (
    <div className="mb-6 rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900/70">
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2 text-sm font-medium text-slate-700 dark:text-slate-300">
          <MapPin className="h-4 w-4" />
          Filtros:
        </div>
        
        <select
          value={filters.farm_id}
          onChange={(e) => updateFilter('farm_id', e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
        >
          <option value="">Todas as Fazendas</option>
          <option value="1">Fazenda Rio Verde</option>
          <option value="2">Fazenda São José</option>
          <option value="3">Fazenda Santa Maria</option>
        </select>

        <select
          value={filters.field_id}
          onChange={(e) => updateFilter('field_id', e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
        >
          <option value="">Todos os Talhões</option>
          <option value="1">Talhão 1</option>
          <option value="2">Talhão 2</option>
          <option value="3">Talhão 3</option>
        </select>

        <select
          value={filters.variety}
          onChange={(e) => updateFilter('variety', e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
        >
          <option value="">Todas as Variedades</option>
          <option value="BMX Potência RR">BMX Potência RR</option>
          <option value="BMX Ativa RR">BMX Ativa RR</option>
          <option value="SYN 13RR">SYN 13RR</option>
        </select>

        <select
          value={filters.season}
          onChange={(e) => updateFilter('season', e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
        >
          <option value="">Todas as Safras</option>
          <option value="2024/2025">2024/2025</option>
          <option value="2023/2024">2023/2024</option>
          <option value="2022/2023">2022/2023</option>
        </select>

        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4 text-slate-500" />
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => updateFilter('date_from', e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
            placeholder="Data Início"
          />
          <span className="text-slate-500">até</span>
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => updateFilter('date_to', e.target.value)}
            className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300"
            placeholder="Data Fim"
          />
        </div>

        {(filters.farm_id || filters.field_id || filters.variety || filters.season || filters.date_from || filters.date_to) && (
          <button
            onClick={clearFilters}
            className="ml-auto rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
          >
            Limpar Filtros
          </button>
        )}
      </div>
    </div>
  )
}

export function GlobalFilters() {
  return (
    <Suspense fallback={<div className="mb-6 h-16 animate-pulse rounded-2xl bg-slate-200 dark:bg-slate-800" />}>
      <GlobalFiltersContent />
    </Suspense>
  )
}

