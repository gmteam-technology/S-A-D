declare module 'react-grid-layout' {
  import type { ComponentType } from 'react'

  export interface Layout {
    i: string
    x: number
    y: number
    w: number
    h: number
  }

  export type Layouts = Record<string, Layout[]>

  export interface ResponsiveProps {
    className?: string
    layouts: Layouts
    cols?: Record<string, number>
    rowHeight?: number
    isDraggable?: boolean
    isResizable?: boolean
    margin?: [number, number]
    children?: React.ReactNode
  }

  export const Responsive: ComponentType<ResponsiveProps>
  export function WidthProvider<T>(component: ComponentType<T>): ComponentType<T>
}
