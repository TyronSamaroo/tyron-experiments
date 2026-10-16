describe('Sample test', () => {
    it('visits the base URL', () => {
      cy.visit('/')
      cy.log('✅ Cypress + TS working!')
    })
  })