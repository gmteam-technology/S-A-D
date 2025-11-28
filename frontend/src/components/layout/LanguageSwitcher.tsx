"use client"

import { useLocale } from '@/contexts/locale-context'

export function LanguageSwitcher() {
  const { locale, setLocale } = useLocale()
  return (
    <div className="flex items-center rounded-full border border-slate-200 bg-white/70 p-1 text-xs font-semibold text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
      {(['pt', 'en'] as const).map((lang) => (
        <button
          key={lang}
          onClick={() => setLocale(lang)}
          className={`rounded-full px-3 py-1 transition ${locale === lang ? 'bg-brand-500 text-white shadow' : ''}`}
        >
          {lang.toUpperCase()}
        </button>
      ))}
    </div>
  )
}
