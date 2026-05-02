# Common Issues in Kiro Powers

This steering file catalogs frequently seen problems in Kiro Powers with examples of bad vs. good patterns and quick-fix guidance. Use this as a reference when diagnosing or fixing specific issues found during evaluation.

---

## Frontmatter Issues

### Invalid Frontmatter Fields

Powers only support 5 frontmatter fields. Any others are invalid and will be ignored or cause issues.

**Bad:**
```yaml
---
name: "my-power"
displayName: "My Power"
description: "Does things"
version: "1.0.0"
tags: ["utility"]
repository: "https://github.com/user/repo"
license: "MIT"
---
```

**Good:**
```yaml
---
name: "my-power"
displayName: "My Power"
description: "Does things"
keywords: ["specific-keyword", "another-keyword"]
author: "Your Name"
---
```

**Fix:** Remove `version`, `tags`, `repository`, `license`, and any other non-standard fields. The only valid fields are: `name`, `displayName`, `description`, `keywords`, `author`.

### Missing Required Fields

All three required fields must be present.

**Bad:**
```yaml
---
name: "my-power"
description: "Does things"
---
```

**Good:**
```yaml
---
name: "my-power"
displayName: "My Power"
description: "Does things"
---
```

**Fix:** Add the missing `displayName` field.

### Name Not in Kebab-Case

**Bad:** `name: "MyPower"`, `name: "my_power"`, `name: "My Power"`

**Good:** `name: "my-power"`

**Fix:** Convert to lowercase with hyphens separating words.

---

## Keyword Issues

### Overly Broad Keywords

Broad keywords cause false-positive activations, annoying users and leading to uninstallation.

**Bad:**
```yaml
keywords: ["test", "debug", "help", "api", "data", "tool"]
```

**Good:**
```yaml
keywords: ["playwright", "functional testing", "e2e testing", "test automation", "browser testing"]
```

**Fix:** Replace generic terms with specific ones related to the power's domain. Ask: "Would a user searching for this keyword specifically want THIS power?"

### Too Few Keywords

**Bad:**
```yaml
keywords: ["terraform"]
```

**Good:**
```yaml
keywords: ["terraform", "infrastructure as code", "iac", "hcl", "terraform cli", "terraform plan"]
```

**Fix:** Add 5-7 keywords including the tool name, its domain, common abbreviations, and key features.

### Duplicate or Redundant Keywords

**Bad:**
```yaml
keywords: ["playwright", "playwright testing", "playwright tests", "playwright test"]
```

**Good:**
```yaml
keywords: ["playwright", "functional testing", "e2e testing", "test automation", "browser testing"]
```

**Fix:** Use distinct terms that cover different search intents rather than variations of the same word.

---

## Description Issues

### Too Long or Vague

**Bad:**
```
description: "This power is a comprehensive tool that helps developers with various aspects of their development workflow including but not limited to testing, debugging, deployment, and monitoring of applications across multiple environments and platforms."
```

**Good:**
```
description: "Automate functional testing with Playwright. Guides test structure, Page Object Model, locator strategies, and CI integration following industry best practices."
```

**Fix:** Limit to 3 sentences max. Focus on what the power does and the value it provides. Use active voice.

### Implementation-Focused Instead of Value-Focused

**Bad:**
```
description: "Contains POWER.md with documentation and steering files for workflows. Uses mcp.json to configure the server."
```

**Good:**
```
description: "Generate formatted release notes from git commits with categorized changes and version tracking."
```

**Fix:** Describe what the user gets, not how the power is built.

---

## Documentation Issues

### Missing Overview

The overview is the first thing agents and users read. Without it, they can't understand the power's purpose.

**Fix:** Add an Overview section with 2-3 paragraphs explaining what the power does, why it's useful, and its key capabilities.

### Placeholder Text Left In

**Bad:**
```markdown
## Troubleshooting

### Error: "{common error message}"
**Cause:** {why this happens}
**Solution:**
1. {diagnostic step}
2. {fix step}
```

**Good:**
```markdown
## Troubleshooting

### Error: "Connection refused"
**Cause:** The MCP server failed to start, usually due to missing dependencies.
**Solution:**
1. Verify the package is installed: `npx -y @package/name`
2. Check that required environment variables are set
3. Restart Kiro and try again
```

**Fix:** Replace all `{placeholder}` text with real content. If you don't know the actual values, research them or ask the user.

### Incomplete Code Examples

**Bad:**
```typescript
// Set up the test
// ... configuration here ...

test('example', async () => {
  // TODO: add test logic
});
```

**Good:**
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

**Fix:** Provide complete, runnable examples. Include imports, setup, and assertions. No `...` or `TODO` markers.

### Missing Troubleshooting Section

Many powers skip troubleshooting, which leaves users stuck when things go wrong.

**Fix:** Add a Troubleshooting section with at least 2-3 common problems. For each problem, document:
- The error message or symptom
- Why it happens
- Step-by-step solution

### Thin Best Practices

**Bad:**
```markdown
## Best Practices
- Follow best practices
- Write good code
- Test your work
```

**Good:**
```markdown
## Best Practices
- Name tests descriptively: 'user can reset password via email link' not 'test 1'
- Group related tests with test.describe for logical organization
- Use test.beforeEach for shared setup like navigation and login
- Keep tests focused — one behavior per test
- Use web-first assertions that auto-wait instead of manual waits
```

**Fix:** Make practices specific, actionable, and relevant to the power's domain.

---

## Structure Issues

### POWER.md Too Large Without Steering Files

If POWER.md exceeds ~500 lines and the power has no steering files, it's loading too much context at once.

**Fix:** Identify independent sections that could be moved to steering files. Keep the overview, quick start, and essential reference in POWER.md. Move detailed workflows, advanced topics, and reference material to `steering/` files.

### Steering Files Not Listed in POWER.md

If steering files exist but aren't described in POWER.md, agents won't know when to read them.

**Bad:**
```markdown
## Overview
This power helps with testing.
```
(No mention of steering files, but `steering/` directory has 3 files)

**Good:**
```markdown
## Available Steering Files

- **project-setup** — Initialize a Playwright project with proper configuration and folder structure
- **writing-tests** — Translate business requirements into test cases using Playwright's API
- **ci-and-advanced** — Configure CI/CD pipelines, parallel execution, and reporting
```

**Fix:** Add an "Available Steering Files" section listing each file with a clear description of what it covers and when to read it.

### Mismatched Steering References

POWER.md lists steering files that don't exist, or steering files exist that aren't listed.

**Fix:** Audit both POWER.md and the `steering/` directory. Ensure every listed file exists and every existing file is listed.

### Unexpected Files in Power Directory

Power directories should only contain: POWER.md, mcp.json (optional), .gitignore (optional), and steering/ (optional).

**Bad:**
```
my-power/
├── POWER.md
├── mcp.json
├── README.md          ← unexpected
├── package.json       ← unexpected
├── src/               ← unexpected
└── steering/
```

**Fix:** Remove files that don't belong. Powers are documentation, not code projects.

---

## MCP Configuration Issues

### Invalid JSON

**Fix:** Validate the JSON syntax. Common issues: trailing commas, missing quotes, unescaped characters.

### Hardcoded Secrets

**Bad:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "sk-abc123realkey456"
      }
    }
  }
}
```

**Good:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

**Fix:** Replace real secrets with placeholder values. Document how to obtain real values in POWER.md under an "MCP Config Placeholders" section.

### Missing Environment Variable Documentation

If mcp.json references environment variables, POWER.md must explain what they are and how to set them.

**Fix:** Add a Configuration section to POWER.md listing each environment variable with its purpose, whether it's required or optional, and how to obtain the value.

### Mixed Local and Remote Configuration

A server entry should use either `command`/`args` (local) or `url` (remote), never both.

**Fix:** Choose one transport type per server entry.

---

## Usability Issues

### Ambiguous Instructions

**Bad:**
```markdown
You might want to consider setting up the configuration before running the tool.
```

**Good:**
```markdown
Before running the tool, create a configuration file:

1. Create `.tool-config.json` in your project root
2. Add the following content:
   ```json
   { "output": "reports/" }
   ```
3. Run the tool: `npx my-tool analyze`
```

**Fix:** Use imperative language. Be specific about what to do, where to do it, and in what order.

### No Quick Start Path

Users (and agents) need a fast path to get started. If the power jumps straight into detailed reference material, it's hard to use.

**Fix:** Add a Quick Start section near the top of POWER.md with the minimum steps to get the power working.

### Duplicated Content Between POWER.md and Steering

If the same content appears in both POWER.md and a steering file, it wastes context and creates maintenance burden.

**Fix:** Keep overview and essential reference in POWER.md. Move detailed content to steering files. Don't duplicate — reference the steering file instead.

---

## Quick Diagnosis Checklist

Use this for a rapid assessment when you don't need a full evaluation:

1. **Does POWER.md exist with valid frontmatter?** → If no, stop here — critical issue
2. **Are there invalid frontmatter fields?** → Remove them
3. **Is there an Overview section?** → If no, add one
4. **Are keywords specific (not broad)?** → If broad, refine them
5. **Are code examples complete?** → If not, fill them in
6. **Is there a Troubleshooting section?** → If no, add one
7. **Do steering file references match actual files?** → If not, fix the mismatch
8. **For MCP powers: is mcp.json valid JSON?** → If not, fix syntax
9. **For MCP powers: are secrets placeholder'd?** → If not, sanitize them
10. **Any TODO/placeholder text remaining?** → If yes, replace with real content
