describe("Todo App", () => {
    beforeEach(() => {
      cy.visit("http://localhost:3000");
    });

    it("adds a new todo", () => {
      cy.get("input[placeholder='Add a new todo']").type("Learn React{enter}");
      cy.contains("Learn React").should("exist");
    });

    it("marks todo as completed", () => {
      cy.get("input[placeholder='Add a new todo']").type("Study Cypress{enter}");
      cy.contains("Study Cypress").click();
      cy.contains("Study Cypress").should("have.css", "text-decoration").and("include", "line-through");
    });

    it("deletes a todo", () => {
      cy.get("input[placeholder='Add a new todo']").type("Delete me{enter}");
      cy.contains("Delete me").should("exist");
      cy.contains("Delete me").parent().find("button").click();
      cy.contains("Delete me").should("not.exist");
    });
  });
