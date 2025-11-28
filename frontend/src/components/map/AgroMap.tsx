"use client"

import { useEffect, useMemo, useState } from 'react'
import { MapContainer, Polygon, TileLayer, GeoJSON } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw/dist/leaflet.draw.css'
import L from 'leaflet'
import type { FeatureCollection, Polygon as GeoPolygon } from 'geojson'
import { useUiStore } from '@/store/useUiStore'

const talhoes = [
  [
    [-12.5501, -55.9502],
    [-12.5501, -55.9402],
    [-12.5401, -55.9402],
    [-12.5401, -55.9502],
  ],
  [
    [-16.4801, -54.7001],
    [-16.4801, -54.6901],
    [-16.4701, -54.6901],
    [-16.4701, -54.7001],
  ],
]

const layerColors: Record<string, string> = {
  solo: '#8b5cf6',
  ndvi: '#22c55e',
  clima: '#38bdf8',
  produtividade: '#f97316',
}

if (typeof window !== 'undefined') {
  const icon = L.Icon.Default.prototype as L.Icon.Default
  icon.options.shadowSize = [0, 0]
}

export function AgroMap() {
  const { activeLayers, toggleLayer } = useUiStore()
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  const geojson = useMemo<FeatureCollection<GeoPolygon>>(
    () => ({
      type: 'FeatureCollection',
      features: talhoes.map((coords, index) => ({
        type: 'Feature',
        properties: { name: `Talhão ${index + 1}` },
        geometry: {
          type: 'Polygon',
          coordinates: [coords.map((pair) => [pair[1], pair[0]])],
        },
      })),
    }),
    [],
  )

  return (
    <section id="mapa" className="mt-10 rounded-3xl border border-white/70 bg-white/80 p-6 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Mapa Agro</p>
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Talhões, camadas e NDVI</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.keys(layerColors).map((layer) => (
            <button
              key={layer}
              onClick={() => toggleLayer(layer)}
              className={`rounded-full px-4 py-1 text-xs font-semibold capitalize transition ${
                activeLayers.includes(layer)
                  ? 'bg-brand-500 text-white shadow'
                  : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300'
              }`}
            >
              {layer}
            </button>
          ))}
        </div>
      </div>
      <div data-testid="mapa-agro" className="h-[420px] overflow-hidden rounded-3xl border border-slate-100 dark:border-slate-800">
        {mounted ? (
          <MapContainer center={[-13.5, -55]} zoom={5} className="h-full w-full" zoomControl={false}>
            <TileLayer attribution='&copy; OpenStreetMap' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {talhoes.map((polygon, idx) => (
              <Polygon key={idx} pathOptions={{ color: '#22c55e', weight: 2 }} positions={polygon.map((pair) => [pair[0], pair[1]])} />
            ))}
            {activeLayers.includes('solo') && <GeoJSON data={geojson} style={{ color: layerColors.solo, weight: 1, fillOpacity: 0.15 }} />}
            {activeLayers.includes('ndvi') && <GeoJSON data={geojson} style={{ color: layerColors.ndvi, weight: 1.5, fillOpacity: 0.2 }} />}
          </MapContainer>
        ) : (
          <div className="flex h-full items-center justify-center text-slate-500">Carregando mapa...</div>
        )}
      </div>
    </section>
  )
}
