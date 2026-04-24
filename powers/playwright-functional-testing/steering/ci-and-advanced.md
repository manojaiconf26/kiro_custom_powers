# CI/CD and Advanced Patterns

Guide for CI/CD integration, parallel execution, reporting, visual regression, API testing, and accessibility testing with Playwright.

## GitHub Actions CI/CD

### Basic Workflow

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 30
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install chromium --with-deps

      - name: Run Playwright tests
        run: npx playwright test
        env:
          BASE_URL: ${{ vars.BASE_URL }}

      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: test-results
          path: test-results/
          retention-days: 7
```

### Sharded Workflow for Faster CI

Split tests across multiple machines:

```yaml
# .github/workflows/playwright-sharded.yml
name: Playwright Tests (Sharded)

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1/4, 2/4, 3/4, 4/4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install chromium --with-deps

      - name: Run Playwright tests
        run: npx playwright test --shard=${{ matrix.shard }}

      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report-${{ strategy.job-index }}
          path: playwright-report/
          retention-days: 30
```

### CI Best Practices

- **Use Linux runners** — Cheaper and faster than Windows/macOS.
- **Install only needed browsers** — `npx playwright install chromium --with-deps` instead of all browsers.
- **Cache node_modules** — Use `npm ci` with GitHub's built-in caching.
- **Upload reports as artifacts** — Always upload HTML reports and traces for debugging.
- **Set `forbidOnly: !!process.env.CI`** — Prevent `test.only` from accidentally running in CI.
- **Set retries on CI** — `retries: process.env.CI ? 2 : 0` to handle transient failures.
- **Use `workers: 1` on CI** — Or tune based on runner resources.

## Parallel Execution

### File-Level Parallelism (Default)

Playwright runs test files in parallel by default. Each file gets its own worker.

### Test-Level Parallelism

Run tests within a single file in parallel:

```typescript
import { test } from '@playwright/test';

test.describe.configure({ mode: 'parallel' });

test('independent test 1', async ({ page }) => {
  // ...
});

test('independent test 2', async ({ page }) => {
  // ...
});
```

### Serial Execution

When tests must run in order (rare — avoid when possible):

```typescript
test.describe.configure({ mode: 'serial' });

test('step 1: create account', async ({ page }) => {
  // ...
});

test('step 2: verify email', async ({ page }) => {
  // ...
});
```

### Sharding

Split tests across multiple machines:

```bash
# Machine 1
npx playwright test --shard=1/3

# Machine 2
npx playwright test --shard=2/3

# Machine 3
npx playwright test --shard=3/3
```

## Reporting

### Built-in Reporters

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    // HTML report — interactive, best for local debugging
    ['html', { open: 'never' }],

    // List reporter — console output
    ['list'],

    // JUnit — for CI integration (Jenkins, Azure DevOps)
    ['junit', { outputFile: 'test-results/junit.xml' }],

    // JSON — for custom processing
    ['json', { outputFile: 'test-results/results.json' }],

    // Dot — minimal output for CI
    ['dot'],
  ],
});
```

### Viewing Reports

```bash
# Open HTML report
npx playwright show-report

# View trace from a failed test
npx playwright show-trace test-results/test-name/trace.zip
```

### Trace Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    // Collect trace on first retry (recommended for CI)
    trace: 'on-first-retry',

    // Or collect trace always (heavy, use for debugging only)
    // trace: 'on',

    // Or collect trace only when retrying
    // trace: 'retain-on-failure',
  },
});
```

Run with trace locally:

```bash
npx playwright test --trace on
```

## Screenshots in CI/CD

### Automatic Failure Screenshots

Configure in `playwright.config.ts` so every failed test produces a screenshot automatically:

```typescript
use: {
  screenshot: 'only-on-failure',  // Recommended for CI
},
```

Failed test screenshots are saved in `test-results/<test-name>/` and appear in the HTML report.

### Uploading Screenshots as CI Artifacts

Include the `test-results/` directory in your artifact upload to preserve failure screenshots:

```yaml
# GitHub Actions
- uses: actions/upload-artifact@v4
  if: ${{ !cancelled() }}
  with:
    name: test-results
    path: test-results/
    retention-days: 7
```

For on-demand screenshots saved to a custom `screenshots/` directory:

```yaml
- uses: actions/upload-artifact@v4
  if: ${{ !cancelled() }}
  with:
    name: screenshots
    path: screenshots/
    retention-days: 14
```

### Attaching Screenshots to Reports

Embed screenshots directly in the HTML report for easy review:

```typescript
test('critical flow screenshot evidence', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // This screenshot appears in the HTML report under this test
  const screenshot = await page.screenshot({ fullPage: true });
  await test.info().attach('dashboard-state', {
    body: screenshot,
    contentType: 'image/png',
  });
});
```

### Screenshot on Every Test (Audit Trail)

For compliance or audit requirements, capture a screenshot after every test:

```typescript
// playwright.config.ts
use: {
  screenshot: 'on',  // Screenshot after every test (increases storage)
},
```

Or use an `afterEach` hook for more control:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  const screenshot = await page.screenshot({ fullPage: true });
  await testInfo.attach(`${testInfo.title}-final-state`, {
    body: screenshot,
    contentType: 'image/png',
  });
});
```

### Custom Failure Screenshot with Full Page

The default failure screenshot captures the viewport. For full-page failure captures:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    const screenshot = await page.screenshot({ fullPage: true });
    await testInfo.attach('failure-full-page', {
      body: screenshot,
      contentType: 'image/png',
    });
  }
});
```

### Screenshot Naming Conventions for CI

Use structured names so screenshots are easy to find in artifacts:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    const sanitizedTitle = testInfo.title.replace(/\s+/g, '-').toLowerCase();
    const screenshot = await page.screenshot({ fullPage: true });
    await testInfo.attach(`failure-${sanitizedTitle}-${testInfo.retry}`, {
      body: screenshot,
      contentType: 'image/png',
    });
  }
});
```

### Reducing Screenshot Storage on CI

```typescript
// Use JPEG with reduced quality for CI artifacts
await page.screenshot({
  path: `screenshots/${testInfo.title}.jpg`,
  type: 'jpeg',
  quality: 70,  // Lower quality = smaller files
});
```

## Visual Regression Testing

### Screenshot Comparisons

```typescript
test('homepage matches visual snapshot', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot comparison
  await expect(page).toHaveScreenshot('homepage.png');
});

test('product card matches visual snapshot', async ({ page }) => {
  await page.goto('/products');

  // Element-level screenshot comparison
  const productCard = page.getByTestId('product-card').first();
  await expect(productCard).toHaveScreenshot('product-card.png');
});
```

### Updating Snapshots

```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update snapshots for specific test
npx playwright test tests/visual.spec.ts --update-snapshots
```

### Visual Testing Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      // Maximum allowed pixel difference
      maxDiffPixels: 100,

      // Or use percentage threshold
      // maxDiffPixelRatio: 0.01,

      // Animation handling
      animations: 'disabled',
    },
  },
});
```

### Visual Testing Best Practices

- **Disable animations** — Set `animations: 'disabled'` to avoid flaky comparisons.
- **Use consistent viewport sizes** — Define in project config.
- **Test on a single browser first** — Font rendering differs across browsers.
- **Mask dynamic content** — Hide timestamps, avatars, or ads:

```typescript
await expect(page).toHaveScreenshot('dashboard.png', {
  mask: [
    page.getByTestId('timestamp'),
    page.getByTestId('user-avatar'),
  ],
});
```

## API Testing with Playwright

Playwright can test APIs directly without a browser:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Products API', () => {
  test('GET /api/products returns product list', async ({ request }) => {
    const response = await request.get('/api/products');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const products = await response.json();
    expect(products).toHaveLength(10);
    expect(products[0]).toHaveProperty('name');
    expect(products[0]).toHaveProperty('price');
  });

  test('POST /api/products creates a new product', async ({ request }) => {
    const response = await request.post('/api/products', {
      data: {
        name: 'New Product',
        price: 19.99,
        category: 'Electronics',
      },
    });

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(201);

    const product = await response.json();
    expect(product.name).toBe('New Product');
    expect(product.id).toBeDefined();
  });

  test('DELETE /api/products/:id removes a product', async ({ request }) => {
    // Create a product first
    const createResponse = await request.post('/api/products', {
      data: { name: 'Temp Product', price: 9.99 },
    });
    const { id } = await createResponse.json();

    // Delete it
    const deleteResponse = await request.delete(`/api/products/${id}`);
    expect(deleteResponse.ok()).toBeTruthy();

    // Verify it's gone
    const getResponse = await request.get(`/api/products/${id}`);
    expect(getResponse.status()).toBe(404);
  });
});
```

### Combining API and UI Tests

Use API calls for setup, then verify in the UI:

```typescript
test('product created via API appears in the UI', async ({ page, request }) => {
  // Setup via API (fast)
  const response = await request.post('/api/products', {
    data: { name: 'API Created Product', price: 49.99, category: 'Electronics' },
  });
  expect(response.ok()).toBeTruthy();

  // Verify in UI
  await page.goto('/products');
  await expect(page.getByText('API Created Product')).toBeVisible();
  await expect(page.getByText('$49.99')).toBeVisible();
});
```

## Accessibility Testing

### Basic Accessibility Checks

Use `@axe-core/playwright` for automated accessibility scanning:

```bash
npm install -D @axe-core/playwright
```

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no accessibility violations', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });

  test('login page has no accessibility violations', async ({ page }) => {
    await page.goto('/login');

    const results = await new AxeBuilder({ page })
      .include('#login-form')  // Scan specific section
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('product page meets WCAG AA standards', async ({ page }) => {
    await page.goto('/products');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])  // WCAG 2.x Level AA
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

Note: Automated accessibility testing catches common issues but does not replace manual testing with assistive technologies and expert accessibility review for full WCAG compliance.

## Network Interception Patterns

### Monitoring Network Requests

```typescript
test('tracks analytics events', async ({ page }) => {
  const analyticsRequests: string[] = [];

  page.on('request', request => {
    if (request.url().includes('/analytics')) {
      analyticsRequests.push(request.url());
    }
  });

  await page.goto('/');
  await page.getByRole('button', { name: 'Sign up' }).click();

  expect(analyticsRequests.length).toBeGreaterThan(0);
});
```

### Simulating Slow Network

```typescript
test('shows loading state on slow network', async ({ page }) => {
  await page.route('**/api/products', async route => {
    // Delay the response by 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));
    await route.continue();
  });

  await page.goto('/products');
  await expect(page.getByText('Loading...')).toBeVisible();
  await expect(page.getByRole('listitem')).not.toHaveCount(0);
});
```

### Simulating Offline Mode

```typescript
test('shows offline message when network is down', async ({ page, context }) => {
  await page.goto('/');

  // Go offline
  await context.setOffline(true);

  await page.getByRole('button', { name: 'Refresh' }).click();
  await expect(page.getByText('You are offline')).toBeVisible();

  // Go back online
  await context.setOffline(false);
});
```

## Multi-Tab and Multi-Context Testing

### New Tab Handling

```typescript
test('external link opens in new tab', async ({ page, context }) => {
  await page.goto('/');

  // Wait for the new page (tab) to open
  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page.getByRole('link', { name: 'Documentation' }).click(),
  ]);

  await newPage.waitForLoadState();
  await expect(newPage).toHaveURL(/.*docs/);
});
```

### Multiple Users in Same Test

```typescript
test('two users can chat in real time', async ({ browser }) => {
  // Create two independent browser contexts
  const userAContext = await browser.newContext();
  const userBContext = await browser.newContext();

  const userAPage = await userAContext.newPage();
  const userBPage = await userBContext.newPage();

  // User A sends a message
  await userAPage.goto('/chat/room-1');
  await userAPage.getByLabel('Message').fill('Hello from User A');
  await userAPage.getByRole('button', { name: 'Send' }).click();

  // User B sees the message
  await userBPage.goto('/chat/room-1');
  await expect(userBPage.getByText('Hello from User A')).toBeVisible();

  await userAContext.close();
  await userBContext.close();
});
```

## Mobile Testing

### Viewport and Device Emulation

Configure in `playwright.config.ts`:

```typescript
projects: [
  {
    name: 'mobile-chrome',
    use: { ...devices['Pixel 5'] },
  },
  {
    name: 'mobile-safari',
    use: { ...devices['iPhone 12'] },
  },
  {
    name: 'tablet',
    use: { ...devices['iPad (gen 7)'] },
  },
],
```

### Touch and Gesture Testing

```typescript
test('mobile menu opens on tap', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'Mobile-only test');

  await page.goto('/');
  await page.getByRole('button', { name: 'Menu' }).tap();
  await expect(page.getByRole('navigation')).toBeVisible();
});
```

## Geolocation and Permissions

```typescript
test('shows nearby stores based on location', async ({ page, context }) => {
  // Grant geolocation permission and set coordinates
  await context.grantPermissions(['geolocation']);
  await context.setGeolocation({ latitude: 40.7128, longitude: -74.0060 });

  await page.goto('/stores');
  await page.getByRole('button', { name: 'Find Nearby' }).click();

  await expect(page.getByText('New York')).toBeVisible();
});
```

## Performance Monitoring

```typescript
test('page loads within acceptable time', async ({ page }) => {
  const startTime = Date.now();
  await page.goto('/');
  const loadTime = Date.now() - startTime;

  // Assert page loads in under 3 seconds
  expect(loadTime).toBeLessThan(3000);

  // Check Core Web Vitals via Performance API
  const lcp = await page.evaluate(() => {
    return new Promise<number>(resolve => {
      new PerformanceObserver(list => {
        const entries = list.getEntries();
        resolve(entries[entries.length - 1].startTime);
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    });
  });

  expect(lcp).toBeLessThan(2500); // LCP should be under 2.5s
});
```

## Debugging Tips

### Local Debugging

```bash
# Run with Playwright Inspector
npx playwright test --debug

# Debug a specific test
npx playwright test tests/login.spec.ts:15 --debug

# Run with UI mode (time-travel debugging)
npx playwright test --ui

# Run headed to see the browser
npx playwright test --headed
```

### Trace Viewer

```bash
# Record traces
npx playwright test --trace on

# Open trace from report
npx playwright show-report

# Open a specific trace file
npx playwright show-trace test-results/test-name/trace.zip
```

### Console and Network Logging

```typescript
test('debug network issues', async ({ page }) => {
  // Log all console messages
  page.on('console', msg => console.log(`Browser console: ${msg.text()}`));

  // Log all network requests
  page.on('request', req => console.log(`>> ${req.method()} ${req.url()}`));
  page.on('response', res => console.log(`<< ${res.status()} ${res.url()}`));

  await page.goto('/');
});
```

### Pausing Execution

```typescript
test('debug this test', async ({ page }) => {
  await page.goto('/');

  // Pause here — opens Playwright Inspector
  await page.pause();

  // Continue after manual inspection
  await page.getByRole('button', { name: 'Submit' }).click();
});
```
