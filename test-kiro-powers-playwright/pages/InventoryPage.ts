import { type Page, type Locator, expect } from '@playwright/test';

export class InventoryPage {
  readonly page: Page;
  readonly title: Locator;
  readonly sortDropdown: Locator;
  readonly inventoryItems: Locator;
  readonly cartBadge: Locator;
  readonly cartLink: Locator;
  readonly burgerMenuButton: Locator;
  readonly logoutLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator('[data-test="title"]');
    this.sortDropdown = page.locator('[data-test="product-sort-container"]');
    this.inventoryItems = page.locator('[data-test="inventory-item"]');
    this.cartBadge = page.locator('[data-test="shopping-cart-badge"]');
    this.cartLink = page.locator('[data-test="shopping-cart-link"]');
    this.burgerMenuButton = page.getByRole('button', { name: 'Open Menu' });
    this.logoutLink = page.locator('[data-test="logout-sidebar-link"]');
  }

  async expectPageLoaded(): Promise<void> {
    await expect(this.title).toHaveText('Products');
  }

  async sortBy(option: string): Promise<void> {
    await this.sortDropdown.selectOption(option);
  }

  async getItemNames(): Promise<string[]> {
    return this.page.locator('[data-test="inventory-item-name"]').allTextContents();
  }

  async getItemPrices(): Promise<number[]> {
    const priceTexts = await this.page.locator('[data-test="inventory-item-price"]').allTextContents();
    return priceTexts.map((text) => parseFloat(text.replace('$', '')));
  }

  async getFirstItemName(): Promise<string> {
    return this.page.locator('[data-test="inventory-item-name"]').first().textContent() as Promise<string>;
  }

  async getFirstItemPrice(): Promise<string> {
    return this.page.locator('[data-test="inventory-item-price"]').first().textContent() as Promise<string>;
  }

  async addItemToCart(itemName: string): Promise<void> {
    const item = this.inventoryItems.filter({ hasText: itemName });
    await item.getByRole('button', { name: 'Add to cart' }).click();
  }

  async removeItemFromCart(itemName: string): Promise<void> {
    const item = this.inventoryItems.filter({ hasText: itemName });
    await item.getByRole('button', { name: 'Remove' }).click();
  }

  async getItemButtonText(itemName: string): Promise<string> {
    const item = this.inventoryItems.filter({ hasText: itemName });
    return item.locator('.btn_inventory').textContent() as Promise<string>;
  }

  async expectCartBadge(count: string): Promise<void> {
    await expect(this.cartBadge).toHaveText(count);
  }

  async expectCartBadgeNotVisible(): Promise<void> {
    await expect(this.cartBadge).not.toBeVisible();
  }

  async goToCart(): Promise<void> {
    await this.cartLink.click();
  }

  async logout(): Promise<void> {
    await this.burgerMenuButton.click();
    await this.logoutLink.click();
  }
}
