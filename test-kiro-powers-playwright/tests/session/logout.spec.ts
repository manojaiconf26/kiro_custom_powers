import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';
import { users } from '../../fixtures/test-data';

test.describe('Application Session', () => {
  test('AC 05.1: user can log out and cannot navigate back', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const inventoryPage = new InventoryPage(page);

    // Log in
    await loginPage.goto();
    await loginPage.login(users.standard.username, users.standard.password);
    await inventoryPage.expectPageLoaded();

    // Log out
    await inventoryPage.logout();

    // Verify redirect to login page
    await expect(page).toHaveURL('https://www.saucedemo.com/');
    await page.screenshot({ path: 'screenshots/logout-redirected.png', fullPage: true });

    // Attempt to navigate back
    await page.goBack();

    // Should not be able to access inventory — either redirected to login or error shown
    await expect(page).toHaveURL('https://www.saucedemo.com/');
    await page.screenshot({ path: 'screenshots/logout-back-button-blocked.png', fullPage: true });
  });
});
