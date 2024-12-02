describe('Responsive Design Test', () => {
    const viewports = [
        { name: 'iPhone 6', width: 375, height: 667 },
        { name: 'iPad', width: 768, height: 1024 },
        { name: 'MacBook 15', width: 1440, height: 900 },
        { name: 'Desktop HD', width: 1920, height: 1080 }
    ];

    viewports.forEach(viewport => {
        it(`should display correctly on ${viewport.name} screen`, () => {
            cy.viewport(viewport.width, viewport.height);
            cy.visit('https://yourwebsite.com'); // Replace with your actual website URL
            
            // Add assertions to check if key elements are present and correctly displayed
            cy.get('header').should('be.visible');
            cy.get('nav').should('be.visible');
            cy.get('.main-content').should('be.visible');
            cy.get('footer').should('be.visible');
            
            // Add more specific assertions based on your layout and design
        });
    });
});
