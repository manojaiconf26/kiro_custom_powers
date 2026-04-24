import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';
import { users } from '../../fixtures/test-data';

test.describe('Product Inventory & Sorting', () => {
  let inventoryPage: InventoryPage;

  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(users.standard.username, users.standard.password);
    inventoryPage = new InventoryPage(page);
    await inventoryPage.expectPageLoaded();
  });

  test('AC 02.1: products can be sorted by price low to high', async ({ page }) => {
    await inventoryPage.sortBy('lohi');

    const prices = await inventoryPage.getItemPrices();
    const sortedPrices = [...prices].sort((a, b) => a - b);
    expect(prices).toEqual(sortedPrices);

    const firstName = await inventoryPage.getFirstItemName();
    const firstPrice = await inventoryPage.getFirstItemPrice();
    expect(firstName).toBe('Sauce Labs Onesie');
    expect(firstPrice).toBe('$7.99');
    await page.screenshot({ path: 'screenshots/sort-price-low-to-high.png', fullPage: true });
  });
});
