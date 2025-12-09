import { AppShell } from '@/components/layout/AppShell'
import { DashboardHero } from '@/components/dashboard/DashboardHero'
import { GlobalFilters } from '@/components/dashboard/GlobalFilters'
import { KPICards } from '@/components/dashboard/KPICards'
import { DashboardGrid } from '@/components/dashboard/DashboardGrid'
import { PriceWidget } from '@/components/prices/PriceWidget'
import { ScenarioSimulator } from '@/components/scenarios/ScenarioSimulator'
import { ClimatologyPanel } from '@/components/climate/ClimatologyPanel'
import { CropPlanner } from '@/components/crops/CropPlanner'
import { UploadWizard } from '@/components/etl/UploadWizard'
import { ReportCenter } from '@/components/reports/ReportCenter'
import { AgroMapClient } from '@/components/map/AgroMapClient'

export default function Home() {
  return (
    <AppShell>
      <DashboardHero />
      <GlobalFilters />
      <KPICards />
      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <DashboardGrid />
        </div>
        <div>
          <PriceWidget />
        </div>
      </div>
      <ScenarioSimulator />
      <ClimatologyPanel />
      <CropPlanner />
      <AgroMapClient />
      <UploadWizard />
      <ReportCenter />
    </AppShell>
  )
}
