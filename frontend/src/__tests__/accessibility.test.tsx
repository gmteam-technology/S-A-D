import { render } from '@testing-library/react'
import { axe } from 'jest-axe'
import { DashboardHero } from '@/components/dashboard/DashboardHero'
import { LocaleProvider } from '@/contexts/locale-context'

const wrapper = ({ children }: { children: React.ReactNode }) => <LocaleProvider>{children}</LocaleProvider>

describe('Acessibilidade do dashboard', () => {
  it('não apresenta violações no hero', async () => {
    const { container } = render(<DashboardHero />, { wrapper })
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
