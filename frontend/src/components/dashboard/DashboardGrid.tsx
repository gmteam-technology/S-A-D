"use client"

import { useState } from 'react'
import { Responsive, WidthProvider, Layouts } from 'react-grid-layout'
import { ClimateWidget } from './ClimateWidget'
import { EconomicWidget } from './EconomicWidget'
import { RainfallWidget } from './RainfallWidget'
import 'react-grid-layout/css/styles.css'
import 'react-resizable/css/styles.css'

const ResponsiveGridLayout = WidthProvider(Responsive)

const layouts: Layouts = {
  lg: [
    { i: 'climate', x: 0, y: 0, w: 4, h: 7 },
    { i: 'economy', x: 4, y: 0, w: 4, h: 7 },
    { i: 'rain', x: 8, y: 0, w: 4, h: 7 },
  ],
}

export function DashboardGrid() {
  const [currentLayouts] = useState(layouts)

  return (
    <section className="rounded-3xl border border-white/70 bg-white/80 p-2 shadow-card dark:border-slate-800 dark:bg-slate-900/70">
      <ResponsiveGridLayout
        className="layout"
        layouts={currentLayouts}
        rowHeight={30}
        cols={{ lg: 12, md: 12, sm: 6, xs: 4, xxs: 2 }}
        isDraggable
        isResizable
        margin={[16, 16]}
      >
        <div key="climate" className="h-full"><ClimateWidget /></div>
        <div key="economy" className="h-full"><EconomicWidget /></div>
        <div key="rain" className="h-full"><RainfallWidget /></div>
      </ResponsiveGridLayout>
    </section>
  )
}
