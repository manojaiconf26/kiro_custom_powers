---
name: "playwright-functional-testing"
displayName: "Functional Test Automation with Playwright"
description: "Create automated functional tests for business requirements using Playwright. Guides test structure, Page Object Model, locator strategies, assertions, and CI integration following industry best practices."
keywords: ["playwright", "functional testing", "e2e testing", "test automation", "browser testing"]
author: "Manoj Kumar S"
---

# Functional Test Automation with Playwright

## Overview

This power helps you create well-structured, maintainable automated functional tests using Playwright. It translates business requirements into reliable end-to-end test suites that verify user-visible behavior across browsers.

The power covers the full lifecycle of test automation: project setup, writing tests with the Page Object Model pattern, choosing resilient locators, writing meaningful assertions, managing test data, and integrating with CI/CD pipelines.

All guidance follows the official Playwright best practices and proven test automation standards.

## Available Steering Files

This power includes focused guides for different aspects of test automation:

- **project-setup** — Initialize a Playwright project with proper configuration, folder structure, and TypeScript support
- **writing-tests** — Translate business requirements into test cases using Playwright's API, locators, assertions, and hooks
- **page-object-model** — Implement the Page Object Model pattern for maintainable, reusable test code
- **ci-and-advanced** — Configure CI/CD pipelines, parallel execution, reporting, visual regression, and API testing

Read a specific steering file when you need detailed guidance on that topic.

## Core Principles

These principles apply to every test you write:

1. **Test user-visible behavior** — Verify what end users see and interact with, not implementation details.
2. **Keep tests isolated** — Each test runs independently with its own state. No test depends on another.
3. **Use resilient locators** — Prefer `getByRole`, `getByText`, `getByLabel`, `getByTestId` over CSS selectors or XPath.
4. **Use web-first assertions** — Always `await expect(locator).toBeVisible()` instead of `expect(await locator.isVisible()).toBe(true)`.
5. **Avoid hard waits** — Never use `page.waitForTimeout()`. Rely on Playwright's built-in auto-waiting.
6. **Don't test third-party dependencies** — Mock external services with `page.route()`.
7. **Structure with Page Object Model** — Encapsulate page interactions in dedicated classes for reuse and maintainability.

## Quick Start

### 1. Install Playwright

```bash
npm init playwright@latest
```

This creates:
- `playwright.config.ts` — Configuration file
- `tests/` — Test directory
- `tests-examples/` — Example tests for reference

### 2. Write Your First Test

```typescript
import { test, expect } from '@playwright/test';

test('user can log in successfully', async ({ page }) => {
  await page.goto('/login');

  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('securepassword');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

### 3. Run Tests

```bash
# Run all tests
npx playwright test

# Run in headed mode (see the browser)
npx playwright test --headed

# Run a specific test file
npx playwright test tests/login.spec.ts

# Run with UI mode for debugging
npx playwright test --ui
```

## Locator Priority Guide

Always choose locators in this order of preference:

| Priority | Locator | Example | When to Use |
|----------|---------|---------|-------------|
| 1 | `getByRole` | `page.getByRole('button', { name: 'Submit' })` | Interactive elements with accessible roles |
| 2 | `getByLabel` | `page.getByLabel('Email')` | Form inputs with labels |
| 3 | `getByPlaceholder` | `page.getByPlaceholder('Search...')` | Inputs with placeholder text |
| 4 | `getByText` | `page.getByText('Welcome back')` | Static text content |
| 5 | `getByTestId` | `page.getByTestId('submit-btn')` | When no semantic locator works; requires `data-testid` attribute |
| 6 | CSS/XPath | `page.locator('.btn-primary')` | Last resort only |

### Chaining and Filtering

Narrow locators by chaining and filtering:

```typescript
// Filter a list to find a specific item, then act on it
const product = page.getByRole('listitem').filter({ hasText: 'Product 2' });
await product.getByRole('button', { name: 'Add to cart' }).click();
```

## Assertion Quick Reference

Use web-first assertions that auto-wait:

```typescript
// Visibility
await expect(page.getByText('Success')).toBeVisible();
await expect(page.getByText('Error')).toBeHidden();

// Text content
await expect(page.getByRole('heading')).toHaveText('Dashboard');
await expect(page.getByRole('alert')).toContainText('saved');

// Input values
await expect(page.getByLabel('Email')).toHaveValue('user@example.com');

// Element state
await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
await expect(page.getByRole('checkbox')).toBeChecked();

// URL and title
await expect(page).toHaveURL(/.*dashboard/);
await expect(page).toHaveTitle('My App - Dashboard');

// Count
await expect(page.getByRole('listitem')).toHaveCount(5);

// Soft assertions (don't stop the test on failure)
await expect.soft(page.getByTestId('status')).toHaveText('Active');
```

## Translating Business Requirements to Tests

When given a business requirement, follow this process:

1. **Identify the user story** — Who is the user? What action do they perform? What outcome do they expect?
2. **Define test scenarios** — Happy path, edge cases, error cases, boundary conditions.
3. **Map to page interactions** — Which pages are involved? What elements does the user interact with?
4. **Write the test** — Use `test.describe` for grouping, clear test names, and the Arrange-Act-Assert pattern.
5. **Add assertions** — Verify the expected outcome from the user's perspective.

### Example: Business Requirement to Test

**Requirement:** "As a user, I can add items to my shopping cart and see the updated total."

```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/products');
  });

  test('user can add an item to the cart and see updated total', async ({ page }) => {
    // Arrange: find a product
    const product = page.getByRole('listitem').filter({ hasText: 'Wireless Mouse' });

    // Act: add to cart
    await product.getByRole('button', { name: 'Add to cart' }).click();

    // Assert: cart shows updated count and total
    await expect(page.getByTestId('cart-count')).toHaveText('1');
    await expect(page.getByTestId('cart-total')).toContainText('$29.99');
  });

  test('user sees empty cart message when no items added', async ({ page }) => {
    await page.getByRole('link', { name: 'Cart' }).click();
    await expect(page.getByText('Your cart is empty')).toBeVisible();
  });
});
```

## Test Organization

```
tests/
├── auth/
│   ├── login.spec.ts
│   ├── logout.spec.ts
│   └── registration.spec.ts
├── cart/
│   ├── add-to-cart.spec.ts
│   └── checkout.spec.ts
├── pages/                      # Page Object Model classes
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── CartPage.ts
├── fixtures/                   # Custom fixtures and test data
│   ├── test-data.ts
│   └── auth.fixture.ts
└── playwright.config.ts
```

## Configuration Essentials

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

## Screenshots

Playwright can capture screenshots automatically and on-demand. Use them for failure debugging, visual evidence, and test reporting.

### Configuration (in `playwright.config.ts`)

```typescript
use: {
  // Automatic screenshot capture options:
  screenshot: 'only-on-failure',  // Recommended default
  // screenshot: 'on',            // Every test (heavy, use for audit trails)
  // screenshot: 'off',           // Disabled
},
```

### Capturing Screenshots in Tests

```typescript
// Full page screenshot
await page.screenshot({ path: 'screenshots/homepage.png', fullPage: true });

// Visible viewport only
await page.screenshot({ path: 'screenshots/viewport.png' });

// Screenshot of a specific element
await page.getByTestId('dashboard-chart').screenshot({ path: 'screenshots/chart.png' });
```

### Screenshot on Key Checkpoints

Capture screenshots at important steps for evidence and debugging:

```typescript
test('user completes checkout', async ({ page }) => {
  await page.goto('/cart');
  await page.screenshot({ path: 'screenshots/checkout-step-1-cart.png' });

  await page.getByRole('button', { name: 'Proceed to Checkout' }).click();
  await page.screenshot({ path: 'screenshots/checkout-step-2-shipping.png' });

  // ... fill shipping info ...
  await page.getByRole('button', { name: 'Place Order' }).click();
  await expect(page.getByText('Order Confirmed')).toBeVisible();
  await page.screenshot({ path: 'screenshots/checkout-step-3-confirmation.png' });
});
```

### Attaching Screenshots to Test Reports

Use `test.info().attach()` to embed screenshots directly in the HTML report:

```typescript
test('dashboard loads correctly', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // Attach screenshot to the HTML report
  const screenshot = await page.screenshot();
  await test.info().attach('dashboard-loaded', {
    body: screenshot,
    contentType: 'image/png',
  });
});
```

### Visual Comparison Screenshots

```typescript
// Compare against a baseline snapshot (creates baseline on first run)
await expect(page).toHaveScreenshot('homepage.png');

// Element-level comparison
await expect(page.getByTestId('product-card').first()).toHaveScreenshot('product-card.png');

// With tolerance options
await expect(page).toHaveScreenshot('dashboard.png', {
  maxDiffPixels: 100,
  mask: [page.getByTestId('timestamp')],  // Mask dynamic content
});
```

See the **ci-and-advanced** steering file for full visual regression testing details.

## Best Practices Summary

- Name tests descriptively: `'user can reset password via email link'` not `'test 1'`
- Group related tests with `test.describe`
- Use `test.beforeEach` for shared setup (navigation, login)
- Use `test.afterEach` for cleanup when needed
- Keep tests focused — one behavior per test
- Use `test.slow()` to triple the timeout for known slow tests
- Use `test.skip()` or `test.fixme()` for tests that need attention
- Use `test.step()` to break complex tests into labeled steps
- Run tests in parallel by default; use `test.describe.serial` only when order matters
- Capture screenshots on failure and at key checkpoints for debugging evidence
- Attach screenshots to test reports with `test.info().attach()` for audit trails
- Capture traces on first retry for CI debugging
- Use TypeScript for better IDE support and early error detection
- Lint tests with `@typescript-eslint/no-floating-promises` to catch missing `await`

## Troubleshooting

### Flaky Tests
- Replace `page.waitForTimeout()` with proper locator waits
- Use `await expect(locator).toBeVisible()` before interacting
- Mock unstable external APIs with `page.route()`
- Check for race conditions in test data setup

### Slow Tests
- Run tests in parallel (`fullyParallel: true`)
- Reuse authentication state with `storageState`
- Only install browsers you need on CI
- Use `test.describe.configure({ mode: 'parallel' })` for independent tests in one file

### Locator Issues
- Use Playwright's codegen to generate locators: `npx playwright codegen <url>`
- Use the VS Code extension's "Pick Locator" feature
- Prefer `getByRole` and `getByLabel` over CSS selectors
- Use `data-testid` attributes when no semantic locator is available

---

**Framework:** Playwright
**Language:** TypeScript (recommended) / JavaScript
**Official Docs:** https://playwright.dev
