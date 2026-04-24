# Project Setup Guide

Detailed guide for initializing and configuring a Playwright functional test project.

## Initialization

### New Project

Run the Playwright installer to scaffold the project:

```bash
npm init playwright@latest
```

When prompted, choose:
- **TypeScript** (recommended for better IDE support and type safety)
- **tests** as the test directory name
- **Yes** to add a GitHub Actions workflow
- **Yes** to install Playwright browsers

### Adding to an Existing Project

```bash
npm install -D @playwright/test
npx playwright install
```

Then create the configuration file manually (see below).

## Recommended Folder Structure

Organize tests by feature area, with Page Objects and fixtures separated:

```
project-root/
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── logout.spec.ts
│   │   └── registration.spec.ts
│   ├── products/
│   │   ├── product-listing.spec.ts
│   │   ├── product-search.spec.ts
│   │   └── product-detail.spec.ts
│   ├── cart/
│   │   ├── add-to-cart.spec.ts
│   │   ├── remove-from-cart.spec.ts
│   │   └── checkout.spec.ts
│   └── account/
│       ├── profile.spec.ts
│       └── settings.spec.ts
├── pages/
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   ├── ProductListingPage.ts
│   ├── CartPage.ts
│   └── CheckoutPage.ts
├── fixtures/
│   ├── auth.fixture.ts
│   ├── test-data.ts
│   └── helpers.ts
├── screenshots/                # On-demand and checkpoint screenshots
├── playwright.config.ts
├── package.json
└── tsconfig.json
```

### Naming Conventions

- Test files: `feature-name.spec.ts` (e.g., `login.spec.ts`, `checkout.spec.ts`)
- Page Objects: `PageName.ts` in PascalCase (e.g., `LoginPage.ts`, `CartPage.ts`)
- Fixture files: `name.fixture.ts` (e.g., `auth.fixture.ts`)
- Test data files: `name.data.ts` or `test-data.ts`
- Directories: lowercase kebab-case matching feature areas

## Configuration File

### Full Configuration Template

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './tests',

  // Run tests in parallel
  fullyParallel: true,

  // Fail CI if test.only is left in code
  forbidOnly: !!process.env.CI,

  // Retry failed tests on CI
  retries: process.env.CI ? 2 : 0,

  // Parallel workers
  workers: process.env.CI ? 1 : undefined,

  // Reporters
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
    ...(process.env.CI ? [['junit', { outputFile: 'test-results/junit.xml' }] as const] : []),
  ],

  // Shared settings for all projects
  use: {
    // Base URL for relative navigation
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Collect trace on first retry
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on first retry
    video: 'on-first-retry',

    // Default timeout for actions (click, fill, etc.)
    actionTimeout: 10_000,

    // Default timeout for navigation
    navigationTimeout: 30_000,
  },

  // Global test timeout
  timeout: 30_000,

  // Expect timeout
  expect: {
    timeout: 5_000,
  },

  // Browser projects
  projects: [
    // Setup project for authentication
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },

    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use setup project's auth state
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Mobile viewports
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 12'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],

  // Run local dev server before tests (optional)
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120_000,
  // },
});
```

### Authentication Setup Project

Create a setup file that logs in once and saves the auth state:

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('testuser@example.com');
  await page.getByLabel('Password').fill('testpassword');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for redirect after login
  await page.waitForURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // Save signed-in state
  await page.context().storageState({ path: authFile });
});
```

Add to `.gitignore`:

```
playwright/.auth/
test-results/
playwright-report/
screenshots/
```

## Screenshot Configuration

Playwright supports automatic and on-demand screenshot capture. Configure the strategy in `playwright.config.ts`:

### Global Screenshot Settings

```typescript
// playwright.config.ts — inside the `use` block
use: {
  // Capture a screenshot automatically when a test fails (recommended)
  screenshot: 'only-on-failure',

  // Other options:
  // screenshot: 'on',   // Capture after every test (useful for audit trails)
  // screenshot: 'off',  // Disable automatic screenshots
},
```

### Screenshot Output Location

Automatic screenshots (on failure or `'on'`) are saved inside the `test-results/` directory alongside traces and videos. On-demand screenshots taken with `page.screenshot({ path })` go wherever you specify.

Recommended convention for on-demand screenshots:

```
project-root/
├── screenshots/              # On-demand screenshots from tests
│   ├── checkout-step-1.png
│   ├── checkout-step-2.png
│   └── dashboard.png
├── test-results/             # Auto-generated: failure screenshots, traces, videos
└── playwright-report/        # Auto-generated: HTML report
```

### Full-Page vs Viewport Screenshots

```typescript
// Viewport only (default) — captures what's visible
await page.screenshot({ path: 'screenshots/viewport.png' });

// Full page — scrolls and captures the entire page
await page.screenshot({ path: 'screenshots/full-page.png', fullPage: true });
```

### Screenshot Quality and Format

```typescript
// JPEG with quality setting (smaller files, good for CI artifacts)
await page.screenshot({
  path: 'screenshots/dashboard.jpg',
  type: 'jpeg',
  quality: 80,
});

// PNG (default, lossless — best for visual comparisons)
await page.screenshot({
  path: 'screenshots/dashboard.png',
  type: 'png',
});
```

### Clipping a Region

```typescript
// Capture a specific rectangular area of the page
await page.screenshot({
  path: 'screenshots/header-region.png',
  clip: { x: 0, y: 0, width: 1280, height: 100 },
});
```

### Hiding Elements Before Screenshot

```typescript
// Hide dynamic content (ads, banners, chat widgets) before capturing
await page.evaluate(() => {
  document.querySelectorAll('.cookie-banner, .chat-widget').forEach(el => {
    (el as HTMLElement).style.display = 'none';
  });
});
await page.screenshot({ path: 'screenshots/clean-page.png', fullPage: true });
```

### Visual Comparison Baseline Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,           // Allow up to 100 pixels to differ
      // maxDiffPixelRatio: 0.01,   // Or allow 1% of pixels to differ
      animations: 'disabled',       // Freeze animations for stable comparisons
      threshold: 0.2,               // Per-pixel color difference threshold (0-1)
    },
    toMatchSnapshot: {
      maxDiffPixelRatio: 0.01,
    },
  },
});
```

## TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": ".",
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["pages/*"],
      "@fixtures/*": ["fixtures/*"],
      "@tests/*": ["tests/*"]
    }
  },
  "include": ["tests/**/*.ts", "pages/**/*.ts", "fixtures/**/*.ts", "playwright.config.ts"],
  "exclude": ["node_modules"]
}
```

## ESLint Configuration for Tests

Install the linting dependency:

```bash
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

Add the rule to catch missing `await` on Playwright API calls:

```json
// .eslintrc.json (relevant rules)
{
  "rules": {
    "@typescript-eslint/no-floating-promises": "error"
  }
}
```

## Environment Variables

Create a `.env` file for local development (add to `.gitignore`):

```bash
# .env
BASE_URL=http://localhost:3000
TEST_USER_EMAIL=testuser@example.com
TEST_USER_PASSWORD=testpassword
```

Load in config or fixtures:

```typescript
import dotenv from 'dotenv';
dotenv.config();

// Use in tests
const baseURL = process.env.BASE_URL || 'http://localhost:3000';
```

## Custom Fixtures

Create reusable fixtures for common test needs:

```typescript
// fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type AuthFixtures = {
  authenticatedPage: ReturnType<typeof base['page']>;
  loginPage: LoginPage;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },
});

export { expect };
```

## Useful Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "test": "npx playwright test",
    "test:headed": "npx playwright test --headed",
    "test:ui": "npx playwright test --ui",
    "test:debug": "npx playwright test --debug",
    "test:chromium": "npx playwright test --project=chromium",
    "test:firefox": "npx playwright test --project=firefox",
    "test:webkit": "npx playwright test --project=webkit",
    "test:mobile": "npx playwright test --project=mobile-chrome --project=mobile-safari",
    "test:report": "npx playwright show-report",
    "test:codegen": "npx playwright codegen",
    "test:trace": "npx playwright test --trace on",
    "test:lint": "eslint tests/ pages/ fixtures/ --ext .ts"
  }
}
```

## Verifying the Setup

After setup, verify everything works:

```bash
# Install browsers
npx playwright install

# Run the example test
npx playwright test

# Open the HTML report
npx playwright show-report

# Launch codegen to verify browser works
npx playwright codegen http://localhost:3000
```

Expected output: all example tests pass, HTML report opens in browser.
