describe('Tic-Tac-Toe', () => {
    beforeEach(() => cy.visit('/'));

    it('X wins with top row', () => {
      cy.get('[aria-label="cell-0"]').click();
      cy.get('[aria-label="cell-3"]').click();
      cy.get('[aria-label="cell-1"]').click();
      cy.get('[aria-label="cell-4"]').click();
      cy.get('[aria-label="cell-2"]').click();
      cy.contains('Winner: X').should('be.visible');
    });

    it('can reset', () => {
        cy.get('[aria-label="cell-0"]').click();  // Click one cell
        cy.get('button').contains('Reset').click();  // Click reset button
        cy.get('[aria-label^="cell-"]').should('have.length', 9).each(($el) => {
          cy.wrap($el).should('have.text', '');  // Check all cells are empty
        });
        cy.contains('Next player: X').should('be.visible');  // Check status
      });
  });