describe('Dashboard Agro', () => {
  it('exibe cards principais', () => {
    cy.visit('/')
    cy.findByTestId('widget-clima').should('exist')
    cy.findByTestId('widget-economia').should('exist')
    cy.findByTestId('mapa-agro').should('exist')
  })
})
