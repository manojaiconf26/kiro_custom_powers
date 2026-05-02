---
name: "skill-agent-builder"
displayName: "Kiro Skill & Agent Builder"
description: "Create, update, and maintain Kiro agent skills (open standard), steering files, custom agents, and hooks. Converts prompts and rules templates to Kiro skills and steering. Use whenever users want to build skills, create steering files, convert existing prompts to skills, or set up agent hooks and custom agents."
keywords: ["skill", "steering", "hooks", "custom agent", "skill builder", "prompt conversion", "q developer"]
author: "Kiro Community"
---

# Kiro Skill & Agent Builder

A comprehensive power for creating, updating, and maintaining Kiro agent artifacts: skills, steering files, custom agents, and hooks.

## Overview

Kiro Skill Builder helps you produce well-structured agent artifacts through a guided, suggestion-first workflow. Before implementing anything, it analyzes your intent, proposes an architecture, and produces a decision log explaining why that design was chosen. Only after your confirmation does it generate the output.

**What it produces:**
- Agent Skills (open standard SKILL.md format with references, scripts, and assets)
- Steering files (always-on, conditional, or manual inclusion)
- Custom agents (optional, for specialized sub-agent workflows)
- Agent hooks (optional, for event-driven automation)

**What it converts:**
- Q Developer prompts and rules templates into Kiro skills and steering files

## Available Steering Files

This power has a single comprehensive steering file:

- **skill-authoring** — Complete guide covering all workflows: creating skills, updating skills, converting prompts, and creating steering/hooks/agents. Includes all schemas, templates, and validation checklists.

## Workflow Summary

Every workflow runs to completion, then invites the user to iterate:

```
1. Capture Intent     → Understand what the user wants
2. Analyze & Propose  → Determine architecture, list artifacts to produce
3. Decision Log       → Document WHY this design was chosen
4. Implement          → Generate all files
5. Validate & Present → Check structure, show results, invite changes
```

## Quick Start

**Creating a new skill:**
> "I want to create a skill that helps generate API documentation from OpenAPI specs"

**Converting Q Developer prompts:**
> "Convert my Q Developer prompt template for code review into a Kiro skill"

**Adding steering to a project:**
> "Create a steering file for our team's coding standards"

**Setting up hooks:**
> "Create a hook that runs linting when TypeScript files are edited"

## Skill Anatomy (Open Standard)

```
skill-name/
├── SKILL.md              (required — frontmatter + instructions)
├── references/           (optional — docs loaded into context as needed)
│   ├── schemas.md
│   └── api-guide.md
├── scripts/              (optional — executable code for deterministic tasks)
│   ├── validate.py
│   └── transform.js
└── assets/               (optional — templates, icons, fonts used in output)
    └── template.html
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: >
  When to trigger and what it does. Be specific about contexts.
  Include trigger phrases so the skill activates reliably.
---
```

**Required fields:** `name`, `description`
**Optional fields:** `license`, `allowed-tools`, `metadata`, `compatibility`

### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** — Loaded as needed (scripts can execute without loading)

## Steering Files

Steering files live in `.kiro/steering/*.md` and provide persistent context to the agent.

**Inclusion modes:**
- **Always** (default) — Included in every interaction
- **Conditional** (`inclusion: fileMatch`) — Included when matching files are in context
- **Manual** (`inclusion: manual`) — User provides via `#` context key in chat

```yaml
---
inclusion: fileMatch
fileMatchPattern: "*.ts"
---
# TypeScript Standards
...
```

## Agent Hooks

Hooks automate agent actions based on IDE events. They live in `.kiro/hooks/`.

```json
{
  "name": "Lint on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.ts", "*.tsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run lint"
  }
}
```

**Event types:** fileEdited, fileCreated, fileDeleted, userTriggered, promptSubmit, agentStop, preToolUse, postToolUse, preTaskExecution, postTaskExecution

## Custom Agents

Custom agents are specialized sub-agents defined as markdown files. They receive a system prompt and have access to tools, running autonomously to complete delegated tasks.

## Best Practices

- Keep SKILL.md under 500 lines; use references/ for overflow
- Write descriptions that are "pushy" — include specific trigger contexts
- Explain the WHY behind instructions, not just the WHAT
- Use scripts/ for deterministic, repeatable tasks
- Use references/ for large docs that should load on-demand
- Include a table of contents for reference files over 300 lines
- Test skills with realistic prompts before finalizing
- Produce a decision log for every skill to document architectural choices

## Decision Log Format

Every skill creation includes a decision log explaining the design:

```markdown
## Decision Log: {skill-name}

### Intent
What the user wants to accomplish.

### Architecture Chosen
What artifacts are being produced and their structure.

### Rationale
Why this structure was chosen over alternatives.

### Trade-offs
What was considered and rejected, and why.

### Artifacts Produced
- SKILL.md — ...
- references/... — ...
- scripts/... — ...
- .kiro/steering/... — ...
- .kiro/hooks/... — ...
```
