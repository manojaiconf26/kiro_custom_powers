import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';
import { users } from '../../fixtures/test-data';

test.describe('User Authentication', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('AC 01.1: user can log in with valid credentials', async ({ page }) => {
    const inventoryPage = new InventoryPage(page);

    await loginPage.login(users.standard.username, users.standard.password);

    await expect(page).toHaveURL(/.*inventory/);
    await inventoryPage.expectPageLoaded();
    await page.screenshot({ path: 'screenshots/login-success.png', fullPage: true });
  });

  test('AC 01.2: locked out user sees error message', async ({ page }) => {
    await loginPage.login(users.lockedOut.username, users.lockedOut.password);

    await loginPage.expectErrorMessage(
      'Epic sadface: Sorry, this user has been locked out.'
    );
    await page.screenshot({ path: 'screenshots/login-locked-out-error.png', fullPage: true });
  });
});
