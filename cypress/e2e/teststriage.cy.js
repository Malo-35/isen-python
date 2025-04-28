describe('Tester la fonction de tri', () => {
  it("Change l'option de tri", () => {
    cy.visit('/home')

    cy.get('[id^=sort]').select('price_asc')
    cy.wait(3000)
    cy.get('[id^=sort]').select('price_desc')
    cy.wait(3000)
    cy.get('[id^=sort]').select('')
  })
})