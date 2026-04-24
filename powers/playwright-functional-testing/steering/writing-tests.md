# Writing Functional Tests

Detailed guide for translating business requirements into Playwright test cases.

## From Requirements to Tests

### Step-by-Step Process

1. **Read the business requirement** — Identify the user, the action, and the expected outcome.
2. **Break into scenarios** — Happy path first, then edge cases, error handling, and boundary conditions.
3. **Identify pages and elements** — Which pages are involved? What does the user interact with?
4. **Write the test** — Use the Arrange-Act-Assert pattern with descriptive names.
5. **Add assertions** — Verify the outcome from the user's perspective.
6. **Review for isolation** — Ensure the test doesn't depend on other tests.

### Naming Tests

Use descriptive names that read like sentences:

```typescript
// Good — describes user behavior and expected outcome
test('user can add a product to the cart from the product detail page', async ({ page }) => {});
test('login form shows error when password is incorrect', async ({ page }) => {});
test('search results update as user types in the search box', async ({ page }) => {});

// Bad — vague, doesn't describe behavior
test('test cart', async ({ page }) => {});
test('login test 1', async ({ page }) => {});
test('search works', async ({ page }) => {});
```

### Grouping Tests

Use `test.describe` to group related tests:

```typescript
test.describe('User Registration', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
  });

  test('user can register with valid email and password', async ({ page }) => {
    // ...
  });

  test('registration fails with already registered email', async ({ page }) => {
    // ...
  });

  test('registration requires password to meet complexity rules', async ({ page }) => {
    // ...
  });
});
```

## Test Patterns

### Pattern: Form Submission

```typescript
test.describe('Contact Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/contact');
  });

  test('user can submit the contact form with valid data', async ({ page }) => {
    await page.getByLabel('Name').fill('Jane Doe');
    await page.getByLabel('Email').fill('jane@example.com');
    await page.getByLabel('Message').fill('I have a question about your product.');
    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Thank you for your message')).toBeVisible();
  });

  test('form shows validation errors for empty required fields', async ({ page }) => {
    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Name is required')).toBeVisible();
    await expect(page.getByText('Email is required')).toBeVisible();
  });

  test('form shows error for invalid email format', async ({ page }) => {
    await page.getByLabel('Name').fill('Jane Doe');
    await page.getByLabel('Email').fill('not-an-email');
    await page.getByRole('button', { name: 'Send Message' }).click();

    await expect(page.getByText('Please enter a valid email')).toBeVisible();
  });
});
```

### Pattern: Navigation and Routing

```typescript
test.describe('Navigation', () => {
  test('user can navigate from home to product listing', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: 'Products' }).click();

    await expect(page).toHaveURL(/.*products/);
    await expect(page.getByRole('heading', { name: 'Our Products' })).toBeVisible();
  });

  test('breadcrumb navigation works correctly', async ({ page }) => {
    await page.goto('/products/wireless-mouse');

    await page.getByRole('link', { name: 'Products' }).click();
    await expect(page).toHaveURL(/.*products$/);
  });

  test('404 page shows for invalid routes', async ({ page }) => {
    await page.goto('/nonexistent-page');
    await expect(page.getByText('Page not found')).toBeVisible();
  });
});
```

### Pattern: Search and Filtering

```typescript
test.describe('Product Search', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/products');
  });

  test('user can search for products by name', async ({ page }) => {
    await page.getByPlaceholder('Search products...').fill('wireless mouse');
    await page.getByRole('button', { name: 'Search' }).click();

    await expect(page.getByRole('listitem')).toHaveCount(3);
    await expect(page.getByText('Wireless Mouse Pro')).toBeVisible();
  });

  test('search shows no results message for unmatched query', async ({ page }) => {
    await page.getByPlaceholder('Search products...').fill('xyznonexistent');
    await page.getByRole('button', { name: 'Search' }).click();

    await expect(page.getByText('No products found')).toBeVisible();
  });

  test('user can filter products by category', async ({ page }) => {
    await page.getByRole('combobox', { name: 'Category' }).selectOption('Electronics');

    const products = page.getByRole('listitem');
    await expect(products).not.toHaveCount(0);
  });
});
```

### Pattern: CRUD Operations

```typescript
test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/tasks');
  });

  test('user can create a new task', async ({ page }) => {
    await page.getByRole('button', { name: 'New Task' }).click();
    await page.getByLabel('Title').fill('Write test documentation');
    await page.getByLabel('Description').fill('Document all test patterns');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByText('Task created successfully')).toBeVisible();
    await expect(page.getByText('Write test documentation')).toBeVisible();
  });

  test('user can edit an existing task', async ({ page }) => {
    const task = page.getByRole('listitem').filter({ hasText: 'Write test documentation' });
    await task.getByRole('button', { name: 'Edit' }).click();

    await page.getByLabel('Title').clear();
    await page.getByLabel('Title').fill('Updated task title');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByText('Task updated successfully')).toBeVisible();
    await expect(page.getByText('Updated task title')).toBeVisible();
  });

  test('user can delete a task with confirmation', async ({ page }) => {
    const task = page.getByRole('listitem').filter({ hasText: 'Updated task title' });
    await task.getByRole('button', { name: 'Delete' }).click();

    // Confirm deletion dialog
    await page.getByRole('button', { name: 'Confirm' }).click();

    await expect(page.getByText('Task deleted')).toBeVisible();
    await expect(page.getByText('Updated task title')).toBeHidden();
  });
});
```

### Pattern: Authentication Flows

```typescript
test.describe('Authentication', () => {
  test('user can log in with valid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('correctpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('login fails with incorrect password', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
    await expect(page).toHaveURL(/.*login/);
  });

  test('user can log out', async ({ page }) => {
    // Assume already logged in via storageState
    await page.goto('/dashboard');
    await page.getByRole('button', { name: 'Account menu' }).click();
    await page.getByRole('menuitem', { name: 'Log out' }).click();

    await expect(page).toHaveURL(/.*login/);
  });

  test('user is redirected to login when accessing protected page', async ({ browser }) => {
    // Use a fresh context without auth state
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*login/);

    await context.close();
  });
});
```

### Pattern: Multi-Step Workflows

Use `test.step` to label phases of complex tests:

```typescript
test('user can complete the checkout process', async ({ page }) => {
  await test.step('Add items to cart', async () => {
    await page.goto('/products');
    const product = page.getByRole('listitem').filter({ hasText: 'Wireless Mouse' });
    await product.getByRole('button', { name: 'Add to cart' }).click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');
  });

  await test.step('Go to checkout', async () => {
    await page.getByRole('link', { name: 'Cart' }).click();
    await page.getByRole('button', { name: 'Proceed to Checkout' }).click();
    await expect(page).toHaveURL(/.*checkout/);
  });

  await test.step('Fill shipping information', async () => {
    await page.getByLabel('Full Name').fill('Jane Doe');
    await page.getByLabel('Address').fill('123 Main St');
    await page.getByLabel('City').fill('Springfield');
    await page.getByLabel('Zip Code').fill('62701');
    await page.getByRole('button', { name: 'Continue' }).click();
  });

  await test.step('Complete payment', async () => {
    await page.getByLabel('Card Number').fill('4111111111111111');
    await page.getByLabel('Expiry').fill('12/28');
    await page.getByLabel('CVV').fill('123');
    await page.getByRole('button', { name: 'Place Order' }).click();
  });

  await test.step('Verify order confirmation', async () => {
    await expect(page.getByRole('heading', { name: 'Order Confirmed' })).toBeVisible();
    await expect(page.getByText('Order #')).toBeVisible();
  });
});
```

## Handling Common UI Patterns

### Dialogs and Modals

```typescript
test('confirmation dialog works correctly', async ({ page }) => {
  // Handle browser dialogs
  page.on('dialog', async dialog => {
    expect(dialog.message()).toContain('Are you sure?');
    await dialog.accept();
  });

  await page.getByRole('button', { name: 'Delete Account' }).click();
});

// For custom modals (not browser dialogs)
test('modal opens and closes correctly', async ({ page }) => {
  await page.getByRole('button', { name: 'Open Settings' }).click();

  const modal = page.getByRole('dialog');
  await expect(modal).toBeVisible();
  await expect(modal.getByRole('heading')).toHaveText('Settings');

  await modal.getByRole('button', { name: 'Close' }).click();
  await expect(modal).toBeHidden();
});
```

### Dropdowns and Select Elements

```typescript
test('user can select a country from dropdown', async ({ page }) => {
  // Native <select>
  await page.getByLabel('Country').selectOption('US');
  await expect(page.getByLabel('Country')).toHaveValue('US');

  // Custom dropdown (non-native)
  await page.getByRole('combobox', { name: 'Country' }).click();
  await page.getByRole('option', { name: 'United States' }).click();
  await expect(page.getByRole('combobox', { name: 'Country' })).toHaveText('United States');
});
```

### Tables

```typescript
test('data table displays correct information', async ({ page }) => {
  await page.goto('/users');

  const table = page.getByRole('table');
  const rows = table.getByRole('row');

  // Check header
  await expect(rows.first()).toContainText('Name');
  await expect(rows.first()).toContainText('Email');

  // Check specific row
  const userRow = rows.filter({ hasText: 'Jane Doe' });
  await expect(userRow.getByRole('cell').nth(1)).toHaveText('jane@example.com');

  // Check row count (excluding header)
  await expect(rows).toHaveCount(11); // 10 data rows + 1 header
});
```

### File Upload

```typescript
test('user can upload a profile picture', async ({ page }) => {
  await page.goto('/profile');

  const fileInput = page.getByLabel('Upload Photo');
  await fileInput.setInputFiles('tests/fixtures/test-avatar.png');

  await expect(page.getByText('File uploaded successfully')).toBeVisible();
});
```

### Pagination

```typescript
test('pagination navigates through results', async ({ page }) => {
  await page.goto('/products');

  // Verify first page
  await expect(page.getByRole('listitem')).toHaveCount(10);
  await expect(page.getByText('Page 1 of 5')).toBeVisible();

  // Go to next page
  await page.getByRole('button', { name: 'Next' }).click();
  await expect(page.getByText('Page 2 of 5')).toBeVisible();
  await expect(page.getByRole('listitem')).toHaveCount(10);

  // Go to last page
  await page.getByRole('button', { name: 'Last' }).click();
  await expect(page.getByText('Page 5 of 5')).toBeVisible();
});
```

## Mocking Network Requests

Mock external APIs to keep tests fast and reliable:

```typescript
test('displays products from API', async ({ page }) => {
  // Mock the API response
  await page.route('**/api/products', route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Wireless Mouse', price: 29.99 },
        { id: 2, name: 'Keyboard', price: 49.99 },
      ]),
    })
  );

  await page.goto('/products');
  await expect(page.getByRole('listitem')).toHaveCount(2);
  await expect(page.getByText('Wireless Mouse')).toBeVisible();
});

test('shows error message when API fails', async ({ page }) => {
  await page.route('**/api/products', route =>
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Internal Server Error' }),
    })
  );

  await page.goto('/products');
  await expect(page.getByText('Failed to load products')).toBeVisible();
});
```

## Test Data Management

### Inline Test Data

For simple tests, define data inline:

```typescript
test('user can register', async ({ page }) => {
  const user = {
    name: 'Test User',
    email: `testuser+${Date.now()}@example.com`,
    password: 'SecurePass123!',
  };

  await page.goto('/register');
  await page.getByLabel('Name').fill(user.name);
  await page.getByLabel('Email').fill(user.email);
  await page.getByLabel('Password').fill(user.password);
  await page.getByRole('button', { name: 'Register' }).click();

  await expect(page.getByText(`Welcome, ${user.name}`)).toBeVisible();
});
```

### Shared Test Data File

For data reused across tests:

```typescript
// fixtures/test-data.ts
export const testUsers = {
  standard: {
    email: 'standard@example.com',
    password: 'StandardPass123!',
    name: 'Standard User',
  },
  admin: {
    email: 'admin@example.com',
    password: 'AdminPass123!',
    name: 'Admin User',
  },
};

export const testProducts = {
  mouse: { name: 'Wireless Mouse', price: '$29.99', sku: 'WM-001' },
  keyboard: { name: 'Mechanical Keyboard', price: '$89.99', sku: 'MK-001' },
};
```

### Dynamic Test Data with Unique Values

Avoid collisions in parallel tests:

```typescript
function uniqueEmail(): string {
  return `test+${Date.now()}-${Math.random().toString(36).slice(2, 7)}@example.com`;
}

test('registration with unique email', async ({ page }) => {
  const email = uniqueEmail();
  // ...
});
```

## Handling Timeouts

```typescript
// Increase timeout for a specific test
test('slow report generation', async ({ page }) => {
  test.slow(); // Triples the default timeout

  await page.goto('/reports');
  await page.getByRole('button', { name: 'Generate Report' }).click();
  await expect(page.getByText('Report ready')).toBeVisible();
});

// Custom timeout for a specific assertion
await expect(page.getByText('Processing complete')).toBeVisible({ timeout: 15_000 });
```

## Capturing Screenshots in Tests

Screenshots serve as visual evidence, debugging aids, and documentation of test execution. Use them strategically at key points.

### Screenshot at Key Checkpoints

Capture screenshots at important steps in multi-step workflows:

```typescript
test('user completes the registration flow', async ({ page }) => {
  await page.goto('/register');
  await page.screenshot({ path: 'screenshots/registration-step-1-form.png' });

  await page.getByLabel('Name').fill('Jane Doe');
  await page.getByLabel('Email').fill('jane@example.com');
  await page.getByLabel('Password').fill('SecurePass123!');
  await page.getByRole('button', { name: 'Register' }).click();

  await expect(page.getByText('Verify your email')).toBeVisible();
  await page.screenshot({ path: 'screenshots/registration-step-2-verification.png' });
});
```

### Screenshot on Failure (Manual Pattern)

Capture a screenshot in a `try/catch` or `afterEach` for custom failure handling:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    // Capture and attach a failure screenshot to the report
    const screenshot = await page.screenshot({ fullPage: true });
    await testInfo.attach('failure-screenshot', {
      body: screenshot,
      contentType: 'image/png',
    });
  }
});
```

Note: If `screenshot: 'only-on-failure'` is set in config, Playwright does this automatically. The manual pattern is useful when you need custom naming, full-page capture, or additional context.

### Attaching Screenshots to HTML Reports

Use `test.info().attach()` to embed screenshots directly in the Playwright HTML report:

```typescript
test('dashboard displays all widgets', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.getByTestId('revenue-widget')).toBeVisible();
  await expect(page.getByTestId('users-widget')).toBeVisible();

  // Attach full dashboard screenshot to the report
  const screenshot = await page.screenshot({ fullPage: true });
  await test.info().attach('dashboard-full', {
    body: screenshot,
    contentType: 'image/png',
  });
});
```

### Element-Level Screenshots

Capture specific components instead of the full page:

```typescript
test('chart renders correctly', async ({ page }) => {
  await page.goto('/analytics');
  await expect(page.getByTestId('sales-chart')).toBeVisible();

  // Screenshot just the chart element
  await page.getByTestId('sales-chart').screenshot({
    path: 'screenshots/sales-chart.png',
  });
});
```

### Screenshots in Multi-Step Workflows with test.step

```typescript
test('user completes checkout', async ({ page }) => {
  await test.step('View cart', async () => {
    await page.goto('/cart');
    await page.screenshot({ path: 'screenshots/checkout-1-cart.png' });
  });

  await test.step('Enter shipping info', async () => {
    await page.getByRole('button', { name: 'Proceed to Checkout' }).click();
    await page.getByLabel('Full Name').fill('Jane Doe');
    await page.getByLabel('Address').fill('123 Main St');
    await page.getByRole('button', { name: 'Continue' }).click();
    await page.screenshot({ path: 'screenshots/checkout-2-shipping.png' });
  });

  await test.step('Confirm order', async () => {
    await page.getByRole('button', { name: 'Place Order' }).click();
    await expect(page.getByText('Order Confirmed')).toBeVisible();
    await page.screenshot({ path: 'screenshots/checkout-3-confirmation.png' });
  });
});
```

### Conditional Screenshots for Debugging

Capture extra screenshots only when running in debug or verbose mode:

```typescript
const VERBOSE = process.env.VERBOSE === 'true';

test('product search works', async ({ page }) => {
  await page.goto('/products');
  await page.getByPlaceholder('Search...').fill('wireless mouse');
  await page.getByRole('button', { name: 'Search' }).click();

  if (VERBOSE) {
    await page.screenshot({ path: 'screenshots/search-results.png', fullPage: true });
  }

  await expect(page.getByText('Wireless Mouse Pro')).toBeVisible();
});
```

### Screenshot Best Practices

- **Use `screenshot: 'only-on-failure'` in config** — Automatic failure screenshots with zero test code.
- **Attach to reports** — Use `test.info().attach()` so screenshots appear in the HTML report alongside traces.
- **Use `fullPage: true`** for pages with scrollable content.
- **Capture at key checkpoints** in multi-step workflows for debugging breadcrumbs.
- **Use element screenshots** for component-level verification instead of full-page captures.
- **Add `screenshots/` to `.gitignore`** — On-demand screenshots are ephemeral debugging artifacts.
- **Use JPEG with quality setting** for CI artifacts to reduce storage: `{ type: 'jpeg', quality: 80 }`.
- **Mask or hide dynamic content** (timestamps, ads, avatars) before capturing for stable results.

## Skipping and Annotating Tests

```typescript
// Skip a test
test.skip('feature not yet implemented', async ({ page }) => {});

// Mark as known issue to fix later
test.fixme('flaky on webkit', async ({ page }) => {});

// Conditional skip
test('only runs on chromium', async ({ page, browserName }) => {
  test.skip(browserName !== 'chromium', 'Feature only supported in Chromium');
  // ...
});

// Tag tests for selective execution
test('user can export data @smoke', async ({ page }) => {});
test('user can import CSV @regression', async ({ page }) => {});

// Run tagged tests: npx playwright test --grep @smoke
```
