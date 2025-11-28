"use client"

import { createContext, useContext, useMemo, useState, ReactNode } from 'react'

type Locale = 'pt' | 'en'

const messages = {
  pt: {
    heroTitle: 'Painel Inteligente do Agronegócio',
    heroSubtitle: 'Combine clima, solo, custos e mapas para decidir com precisão.',
  },
  en: {
    heroTitle: 'Smart Agribusiness Control Center',
    heroSubtitle: 'Blend climate, soil, costs and maps to drive confident decisions.',
  },
}

type TranslationKeys = keyof (typeof messages)['pt']

type LocaleContextValue = {
  locale: Locale
  setLocale: (locale: Locale) => void
  t: (key: TranslationKeys) => string
}

const LocaleContext = createContext<LocaleContextValue | undefined>(undefined)

export function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>('pt')
  const value = useMemo(
    () => ({
      locale,
      setLocale,
      t: (key: TranslationKeys) => messages[locale][key],
    }),
    [locale],
  )
  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>
}

export function useLocale() {
  const context = useContext(LocaleContext)
  if (!context) {
    throw new Error('useLocale must be used within LocaleProvider')
  }
  return context
}
