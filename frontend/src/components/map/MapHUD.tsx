"use client"

import { X, Info } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface HUDData {
  type: 'ndvi' | 'soil' | 'productivity' | 'climate'
  value: number
  label: string
  interpretation: string
  thresholds?: {
    low: { max: number; label: string }
    medium: { min: number; max: number; label: string }
    high: { min: number; label: string }
  }
}

interface MapHUDProps {
  data: HUDData | null
  onClose: () => void
}

export function MapHUD({ data, onClose }: MapHUDProps) {
  if (!data) return null

  const getThresholdStatus = () => {
    if (!data.thresholds) return null
    
    const { low, medium, high } = data.thresholds
    if (data.value <= low.max) return { level: 'low', ...low }
    if (data.value >= high.min) return { level: 'high', ...high }
    return { level: 'medium', ...medium }
  }

  const threshold = getThresholdStatus()
  const percentage = data.type === 'ndvi' ? Math.round((data.value + 1) * 50) : Math.round(data.value)

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        className="absolute right-4 top-4 z-[1000] w-80 rounded-2xl border border-slate-200 bg-white/95 p-4 shadow-xl backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/95"
      >
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <Info className="h-5 w-5 text-brand-500" />
            <h3 className="font-semibold text-slate-900 dark:text-white">{data.label}</h3>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-slate-500 transition hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-300"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="mb-3">
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-bold text-slate-900 dark:text-white">{data.value.toFixed(2)}</p>
            {data.type === 'ndvi' && <span className="text-sm text-slate-500">NDVI</span>}
          </div>
          
          {data.type === 'ndvi' && (
            <div className="mt-2">
              <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-emerald-500 transition-all"
                  style={{ width: `${percentage}%` }}
                />
              </div>
              <div className="mt-1 flex justify-between text-xs text-slate-500">
                <span>-1</span>
                <span>0</span>
                <span>+1</span>
              </div>
            </div>
          )}
        </div>

        <div className="mb-3 rounded-lg bg-slate-50 p-3 dark:bg-slate-800/50">
          <p className="text-sm text-slate-700 dark:text-slate-300">{data.interpretation}</p>
        </div>

        {threshold && (
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-700 dark:bg-slate-800/50">
            <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-600 dark:text-slate-400">
              Thresholds de Interpretação:
            </p>
            <div className="space-y-1 text-xs">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-red-500" />
                <span className={threshold.level === 'low' ? 'font-semibold text-slate-900 dark:text-white' : 'text-slate-600 dark:text-slate-400'}>
                  {data.thresholds!.low.label} (&lt; {data.thresholds!.low.max})
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-yellow-500" />
                <span className={threshold.level === 'medium' ? 'font-semibold text-slate-900 dark:text-white' : 'text-slate-600 dark:text-slate-400'}>
                  {data.thresholds!.medium.label} ({data.thresholds!.medium.min} - {data.thresholds!.medium.max})
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-emerald-500" />
                <span className={threshold.level === 'high' ? 'font-semibold text-slate-900 dark:text-white' : 'text-slate-600 dark:text-slate-400'}>
                  {data.thresholds!.high.label} (&gt; {data.thresholds!.high.min})
                </span>
              </div>
            </div>
          </div>
        )}

        <button className="mt-3 w-full rounded-lg bg-brand-500 px-3 py-2 text-sm font-medium text-white transition hover:bg-brand-600">
          Mais sobre {data.label}
        </button>
      </motion.div>
    </AnimatePresence>
  )
}


