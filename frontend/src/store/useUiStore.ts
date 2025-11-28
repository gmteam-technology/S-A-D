import { create } from 'zustand'

type UiState = {
  darkMode: boolean
  toggleDarkMode: () => void
  activeLayers: string[]
  toggleLayer: (layer: string) => void
  draggingEnabled: boolean
  toggleDragging: () => void
}

export const useUiStore = create<UiState>((set, get) => ({
  darkMode: false,
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  activeLayers: ['solo', 'ndvi', 'produtividade'],
  toggleLayer: (layer) =>
    set((state) => ({
      activeLayers: state.activeLayers.includes(layer)
        ? state.activeLayers.filter((l) => l !== layer)
        : [...state.activeLayers, layer],
    })),
  draggingEnabled: true,
  toggleDragging: () => set({ draggingEnabled: !get().draggingEnabled }),
}))
