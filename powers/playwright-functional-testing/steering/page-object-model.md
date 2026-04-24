# Page Object Model Pattern

Detailed guide for implementing the Page Object Model (POM) in Playwright tests for maintainable, reusable test code.

## Why Page Object Model

The Page Object Model encapsulates page-specific locators and interactions in dedicated classes. Benefits:

- **Single source of truth** — When the UI changes, update one class instead of every test.
- **Readable tests** — Tests read like user stories: `loginPage.login(email, password)`.
- **Reusable interactions** — Common flows (login, navigation) are written once.
- **Separation of concerns** — Tests focus on behavior; page objects handle mechanics.

## Base Page Class

Create a base class with shared functionality:

```typescript
// pages/BasePage.ts
import { Page, Locator } from '@playwright/test';

export class BasePage {
  readonly page: Page;
  readonly header: Locator;
  readonly footer: Locator;
  readonly navMenu: Locator;

  constructor(page: Page) {
    this.page = page;
    this.header = page.getByRole('banner');
    this.footer = page.getByRole('contentinfo');
    this.navMenu = page.getByRole('navigation');
  }

  async navigateTo(path: string): Promise<void> {
    await this.page.goto(path);
  }

  async getPageTitle(): Promise<string> {
    return this.page.title();
  }

  async clickNavLink(name: string): Promise<void> {
    await this.navMenu.getByRole('link', { name }).click();
  }

  /** Capture a full-page screenshot with a descriptive name. */
  async takeScreenshot(name: string): Promise<Buffer> {
    return this.page.screenshot({
      path: `screenshots/${name}.png`,
      fullPage: true,
    });
  }

  /** Attach a screenshot to the current test's HTML report. */
  async attachScreenshot(name: string, testInfo: any): Promise<void> {
    const screenshot = await this.page.screenshot({ fullPage: true });
    await testInfo.attach(name, {
      body: screenshot,
      contentType: 'image/png',
    });
  }
}
```

## Page Object Examples

### Login Page

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly signInButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.signInButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password?' });
  }

  async goto(): Promise<void> {
    await this.navigateTo('/login');
  }

  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }

  async expectErrorMessage(message: string): Promise<void> {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectRedirectToDashboard(): Promise<void> {
    await expect(this.page).toHaveURL(/.*dashboard/);
  }
}
```

### Product Listing Page

```typescript
// pages/ProductListingPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class ProductListingPage extends BasePage {
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly categoryFilter: Locator;
  readonly productList: Locator;
  readonly noResultsMessage: Locator;
  readonly sortDropdown: Locator;

  constructor(page: Page) {
    super(page);
    this.searchInput = page.getByPlaceholder('Search products...');
    this.searchButton = page.getByRole('button', { name: 'Search' });
    this.categoryFilter = page.getByRole('combobox', { name: 'Category' });
    this.productList = page.getByRole('listitem');
    this.noResultsMessage = page.getByText('No products found');
    this.sortDropdown = page.getByRole('combobox', { name: 'Sort by' });
  }

  async goto(): Promise<void> {
    await this.navigateTo('/products');
  }

  async searchFor(query: string): Promise<void> {
    await this.searchInput.fill(query);
    await this.searchButton.click();
  }

  async filterByCategory(category: string): Promise<void> {
    await this.categoryFilter.selectOption(category);
  }

  async sortBy(option: string): Promise<void> {
    await this.sortDropdown.selectOption(option);
  }

  async addProductToCart(productName: string): Promise<void> {
    const product = this.productList.filter({ hasText: productName });
    await product.getByRole('button', { name: 'Add to cart' }).click();
  }

  async expectProductCount(count: number): Promise<void> {
    await expect(this.productList).toHaveCount(count);
  }

  async expectProductVisible(productName: string): Promise<void> {
    await expect(this.page.getByText(productName)).toBeVisible();
  }

  async expectNoResults(): Promise<void> {
    await expect(this.noResultsMessage).toBeVisible();
  }
}
```

### Cart Page

```typescript
// pages/CartPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class CartPage extends BasePage {
  readonly cartItems: Locator;
  readonly cartTotal: Locator;
  readonly cartCount: Locator;
  readonly emptyCartMessage: Locator;
  readonly checkoutButton: Locator;

  constructor(page: Page) {
    super(page);
    this.cartItems = page.getByRole('listitem');
    this.cartTotal = page.getByTestId('cart-total');
    this.cartCount = page.getByTestId('cart-count');
    this.emptyCartMessage = page.getByText('Your cart is empty');
    this.checkoutButton = page.getByRole('button', { name: 'Proceed to Checkout' });
  }

  async goto(): Promise<void> {
    await this.navigateTo('/cart');
  }

  async removeItem(productName: string): Promise<void> {
    const item = this.cartItems.filter({ hasText: productName });
    await item.getByRole('button', { name: 'Remove' }).click();
  }

  async updateQuantity(productName: string, quantity: number): Promise<void> {
    const item = this.cartItems.filter({ hasText: productName });
    await item.getByLabel('Quantity').fill(String(quantity));
  }

  async proceedToCheckout(): Promise<void> {
    await this.checkoutButton.click();
  }

  async expectItemCount(count: number): Promise<void> {
    await expect(this.cartItems).toHaveCount(count);
  }

  async expectTotal(total: string): Promise<void> {
    await expect(this.cartTotal).toContainText(total);
  }

  async expectEmpty(): Promise<void> {
    await expect(this.emptyCartMessage).toBeVisible();
  }
}
```

### Checkout Page

```typescript
// pages/CheckoutPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class CheckoutPage extends BasePage {
  readonly fullNameInput: Locator;
  readonly addressInput: Locator;
  readonly cityInput: Locator;
  readonly zipCodeInput: Locator;
  readonly cardNumberInput: Locator;
  readonly expiryInput: Locator;
  readonly cvvInput: Locator;
  readonly continueButton: Locator;
  readonly placeOrderButton: Locator;
  readonly orderConfirmation: Locator;

  constructor(page: Page) {
    super(page);
    this.fullNameInput = page.getByLabel('Full Name');
    this.addressInput = page.getByLabel('Address');
    this.cityInput = page.getByLabel('City');
    this.zipCodeInput = page.getByLabel('Zip Code');
    this.cardNumberInput = page.getByLabel('Card Number');
    this.expiryInput = page.getByLabel('Expiry');
    this.cvvInput = page.getByLabel('CVV');
    this.continueButton = page.getByRole('button', { name: 'Continue' });
    this.placeOrderButton = page.getByRole('button', { name: 'Place Order' });
    this.orderConfirmation = page.getByRole('heading', { name: 'Order Confirmed' });
  }

  async fillShippingInfo(info: {
    fullName: string;
    address: string;
    city: string;
    zipCode: string;
  }): Promise<void> {
    await this.fullNameInput.fill(info.fullName);
    await this.addressInput.fill(info.address);
    await this.cityInput.fill(info.city);
    await this.zipCodeInput.fill(info.zipCode);
    await this.continueButton.click();
  }

  async fillPaymentInfo(info: {
    cardNumber: string;
    expiry: string;
    cvv: string;
  }): Promise<void> {
    await this.cardNumberInput.fill(info.cardNumber);
    await this.expiryInput.fill(info.expiry);
    await this.cvvInput.fill(info.cvv);
  }

  async placeOrder(): Promise<void> {
    await this.placeOrderButton.click();
  }

  async expectOrderConfirmed(): Promise<void> {
    await expect(this.orderConfirmation).toBeVisible();
  }
}
```

## Using Page Objects in Tests

```typescript
// tests/cart/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { ProductListingPage } from '../../pages/ProductListingPage';
import { CartPage } from '../../pages/CartPage';
import { CheckoutPage } from '../../pages/CheckoutPage';

test.describe('Checkout Flow', () => {
  test('user can complete a purchase end-to-end', async ({ page }) => {
    const productListing = new ProductListingPage(page);
    const cart = new CartPage(page);
    const checkout = new CheckoutPage(page);

    await test.step('Browse and add product to cart', async () => {
      await productListing.goto();
      await productListing.addProductToCart('Wireless Mouse');
    });

    await test.step('Review cart and proceed to checkout', async () => {
      await cart.goto();
      await cart.expectItemCount(1);
      await cart.expectTotal('$29.99');
      await cart.proceedToCheckout();
    });

    await test.step('Fill shipping and payment details', async () => {
      await checkout.fillShippingInfo({
        fullName: 'Jane Doe',
        address: '123 Main St',
        city: 'Springfield',
        zipCode: '62701',
      });

      await checkout.fillPaymentInfo({
        cardNumber: '4111111111111111',
        expiry: '12/28',
        cvv: '123',
      });
    });

    await test.step('Place order and verify confirmation', async () => {
      await checkout.placeOrder();
      await checkout.expectOrderConfirmed();
    });
  });
});
```

## Component Page Objects

For reusable UI components that appear on multiple pages:

```typescript
// pages/components/HeaderComponent.ts
import { Page, Locator, expect } from '@playwright/test';

export class HeaderComponent {
  readonly page: Page;
  readonly logo: Locator;
  readonly searchInput: Locator;
  readonly cartIcon: Locator;
  readonly cartBadge: Locator;
  readonly userMenu: Locator;

  constructor(page: Page) {
    this.page = page;
    const header = page.getByRole('banner');
    this.logo = header.getByRole('link', { name: 'Home' });
    this.searchInput = header.getByPlaceholder('Search...');
    this.cartIcon = header.getByRole('link', { name: 'Cart' });
    this.cartBadge = header.getByTestId('cart-badge');
    this.userMenu = header.getByRole('button', { name: 'Account menu' });
  }

  async search(query: string): Promise<void> {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
  }

  async goToCart(): Promise<void> {
    await this.cartIcon.click();
  }

  async openUserMenu(): Promise<void> {
    await this.userMenu.click();
  }

  async logout(): Promise<void> {
    await this.openUserMenu();
    await this.page.getByRole('menuitem', { name: 'Log out' }).click();
  }

  async expectCartCount(count: number): Promise<void> {
    await expect(this.cartBadge).toHaveText(String(count));
  }
}
```

Use the component in page objects:

```typescript
// pages/DashboardPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';
import { HeaderComponent } from './components/HeaderComponent';

export class DashboardPage extends BasePage {
  readonly header: HeaderComponent;
  readonly welcomeMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.header = new HeaderComponent(page);
    this.welcomeMessage = page.getByRole('heading', { level: 1 });
  }

  async goto(): Promise<void> {
    await this.navigateTo('/dashboard');
  }
}
```

## Page Object Best Practices

### Do

- **Define locators in the constructor** — All locators are declared upfront for easy discovery.
- **Return `Promise<void>` for actions** — Keep methods simple and composable.
- **Include `expect` methods** — Page objects can contain assertion helpers like `expectOrderConfirmed()`.
- **Use descriptive method names** — `fillShippingInfo()` not `fillForm()`.
- **Accept data objects for complex inputs** — Pass structured data instead of many parameters.
- **Create component objects** for reusable UI parts (header, sidebar, modals).
- **Use BasePage screenshot helpers** — Call `takeScreenshot()` or `attachScreenshot()` from any page object for consistent capture.

### Don't

- **Don't put test logic in page objects** — No `test()`, `test.describe()`, or test-specific branching.
- **Don't make page objects depend on each other** — Each page object should be self-contained.
- **Don't store state between method calls** — Page objects should be stateless wrappers.
- **Don't use `page.waitForTimeout()`** — Rely on Playwright's auto-waiting.
- **Don't duplicate locators** — If two page objects need the same element, extract a component.

## Using Fixtures with Page Objects

Create custom fixtures that provide pre-built page objects:

```typescript
// fixtures/pages.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { ProductListingPage } from '../pages/ProductListingPage';
import { CartPage } from '../pages/CartPage';
import { CheckoutPage } from '../pages/CheckoutPage';

type PageFixtures = {
  loginPage: LoginPage;
  productListingPage: ProductListingPage;
  cartPage: CartPage;
  checkoutPage: CheckoutPage;
};

export const test = base.extend<PageFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  productListingPage: async ({ page }, use) => {
    await use(new ProductListingPage(page));
  },
  cartPage: async ({ page }, use) => {
    await use(new CartPage(page));
  },
  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
});

export { expect } from '@playwright/test';
```

Use in tests:

```typescript
// tests/cart/checkout.spec.ts
import { test, expect } from '../../fixtures/pages.fixture';

test('user can add product and checkout', async ({ productListingPage, cartPage, checkoutPage }) => {
  await productListingPage.goto();
  await productListingPage.addProductToCart('Wireless Mouse');

  await cartPage.goto();
  await cartPage.expectItemCount(1);
  await cartPage.proceedToCheckout();

  await checkoutPage.fillShippingInfo({
    fullName: 'Jane Doe',
    address: '123 Main St',
    city: 'Springfield',
    zipCode: '62701',
  });

  await checkoutPage.fillPaymentInfo({
    cardNumber: '4111111111111111',
    expiry: '12/28',
    cvv: '123',
  });

  await checkoutPage.placeOrder();
  await checkoutPage.expectOrderConfirmed();
});
```

## File Organization Summary

```
pages/
├── BasePage.ts                    # Shared base class
├── LoginPage.ts                   # Login page interactions
├── DashboardPage.ts               # Dashboard page interactions
├── ProductListingPage.ts          # Product listing interactions
├── CartPage.ts                    # Cart page interactions
├── CheckoutPage.ts                # Checkout page interactions
└── components/                    # Reusable UI components
    ├── HeaderComponent.ts
    ├── SidebarComponent.ts
    └── ModalComponent.ts
```

Each page object file should:
- Import `Page` and `Locator` from `@playwright/test`
- Extend `BasePage` (or stand alone for components)
- Define all locators in the constructor
- Expose methods for user interactions
- Include assertion helpers for common verifications
