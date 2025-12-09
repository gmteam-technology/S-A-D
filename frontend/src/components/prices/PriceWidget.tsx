"use client"

import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, RefreshCw, Clock } from 'lucide-react'
import { api } from '@/lib/api'

interface PriceData {
  soybean: {
    spot: {
      price_r_sc: number
      price_r_t: number
      source: string
      timestamp: string
      last_updated: string
      cache_ttl_seconds: number
    }
    contract: {
      price_r_sc: number
      maturity: string
      source: string
      timestamp: string
    }
  }
  fertilizer: {
    npk_10_10_10: {
      price_r_t: number
      source: string
      timestamp: string
    }
  }
  freight: {
    price_r_t: number
    route: string
    distance_km: number
    source: string
    timestamp: string
  }
}

function formatTimeAgo(timestamp: string): string {
  const now = new Date()
  const time = new Date(timestamp)
  const diffMs = now.getTime() - time.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return 'Agora'
  if (diffMins < 60) return `há ${diffMins} min`
  const diffHours = Math.floor(diffMins / 60)
  return `há ${diffHours}h`
}

export function PriceWidget() {
  const { data: prices, isLoading, refetch } = useQuery<PriceData>({
    queryKey: ['prices', 'current'],
    queryFn: api.getCurrentPrices,
    refetchInterval: 300000, // 5 minutos
    staleTime: 300000
  })

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white/80 p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900/70">
        <div className="h-32 animate-pulse rounded-lg bg-slate-200 dark:bg-slate-800" />
      </div>
    )
  }

  if (!prices) return null

  const spotPrice = prices.soybean.spot
  const contractPrice = prices.soybean.contract
  const fertilizerPrice = prices.fertilizer.npk_10_10_10
  const freightPrice = prices.freight

  return (
    <motion.div
      className="rounded-2xl border border-slate-200 bg-gradient-to-br from-amber-50 to-white p-5 shadow-sm dark:border-slate-800 dark:from-amber-500/10 dark:to-slate-900/70"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-slate-600 dark:text-slate-400">
            Preços de Mercado
          </p>
          <h3 className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">
            Soja, Fertilizantes & Frete
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-slate-500" />
          <span className="text-xs text-slate-500">
            {formatTimeAgo(spotPrice.last_updated)}
          </span>
          <button
            onClick={() => refetch()}
            className="rounded-lg p-1.5 text-slate-500 transition hover:bg-white/60 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-300"
            title="Atualizar preços"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="space-y-3">
        {/* Soja Spot */}
        <div className="rounded-xl border border-amber-200 bg-white/80 p-3 dark:border-amber-500/30 dark:bg-slate-800/60">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Soja Spot</p>
              <p className="mt-1 text-xl font-bold text-amber-600 dark:text-amber-400">
                R$ {spotPrice.price_r_sc.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}/sc
              </p>
              <p className="text-xs text-slate-500">R$ {spotPrice.price_r_t.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/t</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-slate-500">{spotPrice.source}</p>
              <TrendingUp className="mt-1 h-5 w-5 text-emerald-500" />
            </div>
          </div>
        </div>

        {/* Soja Contrato */}
        <div className="rounded-xl border border-slate-200 bg-white/60 p-3 dark:border-slate-700 dark:bg-slate-800/40">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-600 dark:text-slate-400">
                Soja Contrato ({contractPrice.maturity})
              </p>
              <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">
                R$ {contractPrice.price_r_sc.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/sc
              </p>
            </div>
            <p className="text-xs text-slate-500">{contractPrice.source}</p>
          </div>
        </div>

        {/* Fertilizante */}
        <div className="rounded-xl border border-slate-200 bg-white/60 p-3 dark:border-slate-700 dark:bg-slate-800/40">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Fertilizante NPK 10-10-10</p>
              <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">
                R$ {fertilizerPrice.price_r_t.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/t
              </p>
            </div>
            <p className="text-xs text-slate-500">{fertilizerPrice.source}</p>
          </div>
        </div>

        {/* Frete */}
        <div className="rounded-xl border border-slate-200 bg-white/60 p-3 dark:border-slate-700 dark:bg-slate-800/40">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Frete ({freightPrice.route})</p>
              <p className="mt-1 text-lg font-semibold text-slate-900 dark:text-white">
                R$ {freightPrice.price_r_t.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}/t
              </p>
              <p className="text-xs text-slate-500">{freightPrice.distance_km} km</p>
            </div>
            <p className="text-xs text-slate-500">{freightPrice.source}</p>
          </div>
        </div>
      </div>
    </motion.div>
  )
}


