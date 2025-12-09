import type { NextConfig } from 'next'
import withPWA from 'next-pwa'

const withPwa = withPWA({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
})

const nextConfig: NextConfig = {
  typedRoutes: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  webpack: (config: any, { dev }: { dev: boolean }) => {
    // Configurações para reduzir uso de memória durante o build no Docker
    if (!dev) {
      // Limita o paralelismo para evitar erros de workers no Docker
      config.parallelism = Math.min(config.parallelism || 1, 2)
    }
    return config
  },
  // Configuração turbopack vazia para silenciar o aviso
  // (usamos webpack explicitamente via flag --webpack)
  turbopack: {},
}

export default withPwa(nextConfig)
