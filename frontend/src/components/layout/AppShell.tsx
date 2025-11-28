"use client"

import { Menu, Sun, Moon, Bell, Globe } from 'lucide-react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useTheme } from 'next-themes'
import { PropsWithChildren, useEffect, useState } from 'react'
import { LanguageSwitcher } from './LanguageSwitcher'

export function AppShell({ children }: PropsWithChildren) {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      <header className="backdrop-blur-xl supports-[backdrop-filter]:bg-white/70 sticky top-0 z-40 border-b border-white/40 bg-white/60 px-6 py-4 dark:border-slate-800 dark:bg-slate-900/70">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-3">
            <button className="rounded-full border border-slate-200 p-2 text-slate-600 shadow-sm transition hover:bg-white dark:border-slate-700 dark:text-slate-200">
              <Menu className="h-5 w-5" />
            </button>
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">SIAD Agro</p>
              <h1 className="text-lg font-semibold text-slate-900 dark:text-white">Centro de Decisões Inteligentes</h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Link href="#mapa" className="hidden rounded-full bg-brand-500/10 px-4 py-2 text-sm font-medium text-brand-600 transition hover:bg-brand-500/20 dark:text-brand-300 md:inline-flex">
              <Globe className="mr-2 h-4 w-4" />Mapa Agro
            </Link>
            <LanguageSwitcher />
            <button className="rounded-full border border-slate-200 p-2 text-slate-600 transition hover:bg-white dark:border-slate-700 dark:text-slate-200">
              <Bell className="h-5 w-5" />
            </button>
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="rounded-full border border-slate-200 bg-white p-2 text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:shadow dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100"
              aria-label="Alternar tema"
            >
              {mounted && theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </header>
      <motion.main
        className="mx-auto w-full max-w-7xl px-4 pb-16 pt-10 sm:px-6 lg:px-8"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {children}
      </motion.main>
    </div>
  )
}
