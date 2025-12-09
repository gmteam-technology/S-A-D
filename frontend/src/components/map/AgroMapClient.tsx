"use client"

import dynamic from 'next/dynamic'

const AgroMap = dynamic(() => import('./AgroMap').then((mod) => mod.AgroMap), { ssr: false })

export function AgroMapClient() {
  return <AgroMap />
}

