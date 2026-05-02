---
name: "power-evaluator"
displayName: "Power Evaluator"
description: "Evaluate any Kiro Power for quality, completeness, and best practices. Provides structured scoring across documentation, structure, usability, and discoverability with actionable improvement recommendations."
keywords: ["power evaluator", "power review", "power quality", "evaluate power", "power audit"]
author: "Kiro Community"
---

# Power Evaluator

## Overview

Power Evaluator is a structured assessment tool for reviewing any Kiro Power — whether it's a Guided MCP Power or a Knowledge Base Power. It walks you through a comprehensive evaluation covering documentation quality, structural correctness, usability, discoverability, and adherence to Kiro Power best practices.

Use this power when you've built a new power and want to validate it before sharing, when reviewing a power someone else created, or when you want to improve an existing power's quality.

The evaluation produces a scorecard with ratings across multiple dimensions, highlights strengths, flags issues, and provides prioritized recommendations for improvement.

## Available Steering Files

This power includes two focused steering files:

- **evaluation-checklist** — The complete evaluation rubric with scoring criteria, category breakdowns, and the structured evaluation workflow. Read this to perform a full power evaluation.
- **common-issues** — Catalog of frequently seen problems in powers with examples of bad vs. good patterns, and quick-fix guidance. Read this when you need to diagnose or fix specific issues.

## Quick Start

To evaluate a power, point the agent at the power's directory:

> "Evaluate the power at powers/my-power-name"

Or evaluate an installed power:

> "Evaluate the playwright-functional-testing power"

The agent will read the power's files, run through the evaluation checklist, and produce a scorecard with recommendations.

## Evaluation Dimensions

The evaluation covers five core dimensions:

### 1. Structure & Completeness

Does the power have all required files? Is the directory layout correct? Are frontmatter fields valid?

- POWER.md exists with valid frontmatter
- Required fields present: name, displayName, description
- No invalid frontmatter fields (version, tags, repository, license)
- mcp.json present for Guided MCP Powers, absent for Knowledge Base Powers
- Steering files organized properly (if used)
- .gitignore present (if needed)

### 2. Documentation Quality

Is the documentation clear, complete, and useful for both agents and humans?

- Overview explains what the power does and why
- Onboarding section with prerequisites and setup
- Common workflows with step-by-step instructions
- Troubleshooting section with real error scenarios
- Best practices section
- Code examples are complete and runnable
- No placeholder text or TODO markers

### 3. Usability & Agent Experience

Will an agent be able to effectively use this power?

- Clear workflow guidance that agents can follow
- Tool names and parameters documented accurately (for MCP powers)
- Examples show realistic usage scenarios
- Steering files have clear descriptions in POWER.md
- Progressive disclosure — overview in POWER.md, details in steering
- Content is appropriately sized (POWER.md not bloated, steering used when needed)

### 4. Discoverability & Metadata

Will users find this power when they need it?

- Name follows kebab-case convention
- DisplayName is clear and professional (2-5 words, Title Case)
- Description is concise (max 3 sentences) and value-focused
- Keywords are specific and relevant (not overly broad)
- Keywords avoid false-positive triggers (no generic terms like "test", "debug", "help")
- 5-7 keywords provided

### 5. MCP Configuration (Guided MCP Powers only)

Is the MCP server configuration correct and well-documented?

- mcp.json follows the correct schema
- Environment variables documented
- Placeholders used for sensitive values (if sharing)
- Placeholder documentation in POWER.md
- disabledTools used only with documented rationale
- autoApprove used judiciously

## Scoring

Each dimension is rated on a 4-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 4 | Excellent | Meets all criteria, exemplary quality |
| 3 | Good | Meets most criteria, minor improvements possible |
| 2 | Needs Work | Missing important elements, functional but incomplete |
| 1 | Poor | Major gaps, needs significant rework |

**Overall Rating:**
- **20-18**: Ready to share — high quality power
- **17-14**: Good foundation — address flagged items before sharing
- **13-10**: Needs work — several areas require attention
- **Below 10**: Major rework needed — revisit the power-builder guide

For Knowledge Base Powers, the MCP Configuration dimension is excluded and the total is out of 16:
- **16-15**: Ready to share
- **14-12**: Good foundation
- **11-8**: Needs work
- **Below 8**: Major rework needed

## Output Format

The evaluation produces a structured report:

```
# Power Evaluation: {power-name}

## Summary
Type: Guided MCP Power | Knowledge Base Power
Overall Score: X/20 (or X/16 for Knowledge Base)
Rating: Excellent | Good | Needs Work | Poor

## Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Structure & Completeness | X/4 | ... |
| Documentation Quality | X/4 | ... |
| Usability & Agent Experience | X/4 | ... |
| Discoverability & Metadata | X/4 | ... |
| MCP Configuration | X/4 | ... (or N/A) |

## Strengths
- ...

## Issues Found
- [Critical] ...
- [Warning] ...
- [Suggestion] ...

## Recommendations (Prioritized)
1. ...
2. ...
3. ...
```

## Best Practices for Evaluators

- Read ALL files in the power directory before scoring
- Check frontmatter fields against the valid set (name, displayName, description, keywords, author)
- Verify code examples are syntactically correct
- Check that steering file descriptions in POWER.md match actual steering files
- For MCP powers, validate mcp.json schema
- Flag placeholder text, TODO markers, or incomplete sections
- Be specific in recommendations — say what to fix and how
- Prioritize critical issues (broken structure, missing required files) over style suggestions
