import dynamic from 'next/dynamic'
import { AppShell } from '@/components/layout/AppShell'
import { DashboardHero } from '@/components/dashboard/DashboardHero'
import { DashboardGrid } from '@/components/dashboard/DashboardGrid'
import { ScenarioSimulator } from '@/components/scenarios/ScenarioSimulator'
import { ClimatologyPanel } from '@/components/climate/ClimatologyPanel'
import { CropPlanner } from '@/components/crops/CropPlanner'
import { UploadWizard } from '@/components/etl/UploadWizard'
import { ReportCenter } from '@/components/reports/ReportCenter'

const AgroMap = dynamic(() => import('@/components/map/AgroMap').then((mod) => mod.AgroMap), { ssr: false })

export default function Home() {
  return (
    <AppShell>
      <DashboardHero />
      <DashboardGrid />
      <ScenarioSimulator />
      <ClimatologyPanel />
      <CropPlanner />
      <AgroMap />
      <UploadWizard />
      <ReportCenter />
    </AppShell>
  )
}
