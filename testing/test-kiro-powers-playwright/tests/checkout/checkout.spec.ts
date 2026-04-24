import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { InventoryPage } from '../../pages/InventoryPage';
import { CartPage } from '../../pages/CartPage';
import { CheckoutPage } from '../../pages/CheckoutPage';
import { users, products } from '../../fixtures/test-data';

test.describe('Checkout Workflow', () => {
  let inventoryPage: InventoryPage;
  let cartPage: CartPage;
  let checkoutPage: CheckoutPage;

  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(users.standard.username, users.standard.password);
    inventoryPage = new InventoryPage(page);
    cartPage = new CartPage(page);
    checkoutPage = new CheckoutPage(page);
    await inventoryPage.expectPageLoaded();
  });

  test('AC 04.1: checkout shows error when information fields are empty', async ({ page }) => {
    await inventoryPage.addItemToCart(products.backpack);
    await inventoryPage.goToCart();
    await cartPage.checkout();

    // Click continue without filling any fields
    await checkoutPage.clickContinue();
    await checkoutPage.expectErrorMessage('Error: First Name is required');
    await page.screenshot({ path: 'screenshots/checkout-validation-error.png', fullPage: true });
  });

  test('AC 04.2: user can complete an order successfully', async ({ page }) => {
    await inventoryPage.addItemToCart(products.backpack);
    await inventoryPage.goToCart();
    await cartPage.checkout();

    await checkoutPage.fillInformation('John', 'Doe', '12345');
    await checkoutPage.clickContinue();

    // Now on Checkout: Overview page
    await expect(page).toHaveURL(/.*checkout-step-two/);
    await page.screenshot({ path: 'screenshots/checkout-overview.png', fullPage: true });

    await checkoutPage.clickFinish();

    // Verify order completion
    await expect(page).toHaveURL(/.*checkout-complete/);
    await checkoutPage.expectOrderComplete();
    await page.screenshot({ path: 'screenshots/checkout-complete.png', fullPage: true });
  });
});
