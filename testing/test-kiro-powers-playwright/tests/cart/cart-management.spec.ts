import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';
import { users, products } from '../../fixtures/test-data';

test.describe('Shopping Cart Management', () => {
  let inventoryPage: InventoryPage;

  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(users.standard.username, users.standard.password);
    inventoryPage = new InventoryPage(page);
    await inventoryPage.expectPageLoaded();
  });

  test('AC 03.1: user can add a product to the cart', async ({ page }) => {
    await inventoryPage.addItemToCart(products.backpack);

    await inventoryPage.expectCartBadge('1');

    const buttonText = await inventoryPage.getItemButtonText(products.backpack);
    expect(buttonText).toBe('Remove');
    await page.screenshot({ path: 'screenshots/cart-item-added.png', fullPage: true });
  });

  test('AC 03.2: user can remove a product from the cart', async ({ page }) => {
    // First add an item
    await inventoryPage.addItemToCart(products.backpack);
    await inventoryPage.expectCartBadge('1');
    await page.screenshot({ path: 'screenshots/cart-before-remove.png', fullPage: true });

    // Then remove it
    await inventoryPage.removeItemFromCart(products.backpack);

    await inventoryPage.expectCartBadgeNotVisible();

    const buttonText = await inventoryPage.getItemButtonText(products.backpack);
    expect(buttonText).toBe('Add to cart');
    await page.screenshot({ path: 'screenshots/cart-item-removed.png', fullPage: true });
  });
});
