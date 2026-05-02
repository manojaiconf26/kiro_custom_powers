# Skill Authoring — Complete Guide

This is the single steering file for the Kiro Skill Builder power. It covers creating, updating, and converting skills, plus creating steering files, hooks, and custom agents. All schemas and templates are included at the end.

Pick the workflow that matches the user's task and follow it through. Every workflow runs to completion — produce all artifacts, validate, present the result, and then invite the user to request changes.

---

## Table of Contents

- [Workflow A: Create a New Skill](#workflow-a-create-a-new-skill)
- [Workflow B: Update an Existing Skill](#workflow-b-update-an-existing-skill)
- [Workflow C: Convert Prompts to Skills](#workflow-c-convert-prompts-to-skills)
- [Workflow D: Create Steering, Hooks, or Custom Agents](#workflow-d-create-steering-hooks-or-custom-agents)
- [Schemas and Templates](#schemas-and-templates)
- [Validation Checklists](#validation-checklists)

---

# Workflow A: Create a New Skill

## A1: Capture Intent

Start by understanding what the user wants. If the conversation already contains a workflow they want to capture (e.g., "turn this into a skill"), extract answers from the conversation history first.

**Gather these answers:**

1. **Purpose** — What should this skill enable the agent to do?
2. **Trigger context** — When should this skill activate? What phrases or situations?
3. **Output format** — What does the expected output look like?
4. **Complexity** — Is this a simple single-step skill or a multi-step workflow?
5. **Dependencies** — Does it need external tools, APIs, or specific file types?
6. **Bundled resources** — Will it need scripts, reference docs, or asset files?

**Interview tips:**
- Ask about edge cases and input/output formats
- Ask about success criteria — how will the user know it worked?
- Check if there are existing patterns, templates, or examples to follow
- If the user mentions Q Developer prompts or existing rules, switch to Workflow C

---

## A2: Analyze and Propose

Based on the captured intent, determine the skill architecture.

### Skill Structure

```
proposed-skill-name/
├── SKILL.md
├── references/          (if needed)
│   └── {files}
├── scripts/             (if needed)
│   └── {files}
└── assets/              (if needed)
    └── {files}
```

Explain what each file will contain and why it exists.

### Companion Artifacts

Identify whether the skill should also include:

- **Steering files** — If the skill benefits from persistent project-level context (coding standards, team conventions, project-specific rules). Determine specific steering files with their inclusion mode (always, fileMatch, manual).
- **Agent hooks** — If the skill workflow benefits from automated triggers (e.g., run validation on file save, lint after edits). Determine specific hooks with event types and actions.
- **Custom agents** — If the skill delegates complex sub-tasks that benefit from isolated context and specialized instructions. Determine agent definitions with their roles.

### Description Draft

Draft the SKILL.md description field. Make it "pushy" — include specific contexts for when to use the skill, not just what it does. The description is the primary triggering mechanism.

**Good example:**
> "Generate API documentation from OpenAPI specs. Use this skill whenever the user mentions API docs, swagger, OpenAPI, endpoint documentation, or wants to create developer-facing documentation for REST APIs, even if they don't explicitly say 'OpenAPI'."

**Bad example:**
> "Helps with API documentation."

### Naming

- Use kebab-case for the skill name (max 64 characters)
- Name should be descriptive of what the skill does
- Examples: `api-doc-generator`, `code-review-helper`, `data-pipeline-builder`

---

## A3: Decision Log

Produce a decision log documenting the reasoning behind the architecture.

```markdown
## Decision Log: {skill-name}

### Intent
{One paragraph summarizing what the user wants}

### Architecture Chosen
{List all artifacts being produced with brief descriptions}

### Rationale
- Why SKILL.md is structured this way
- Why specific reference files were chosen (or not)
- Why scripts are included (or not)
- Why steering/hooks/agents are included (or not)

### Alternatives Considered
- Alternative 1: {description} — Rejected because {reason}
- Alternative 2: {description} — Rejected because {reason}

### Trade-offs
- {Trade-off 1}
- {Trade-off 2}

### Artifacts Summary
| Artifact | Path | Purpose |
|----------|------|---------|
| SKILL.md | {skill-name}/SKILL.md | {purpose} |
| ... | ... | ... |
```

---

## A4: Implement

Generate all files.

### Write SKILL.md

**Frontmatter:**
```yaml
---
name: {skill-name}
description: >
  {The pushy description from A2}
---
```

**Body structure:**
1. Title and overview (what the skill does, at a high level)
2. When to use (contexts and trigger scenarios — reinforces the description)
3. Step-by-step workflow (the main instructions)
4. Output format (what the result should look like)
5. Examples (input/output pairs showing expected behavior)
6. References to bundled resources (with guidance on when to read them)
7. Edge cases and error handling

**Writing guidelines:**
- Use imperative form for instructions
- Explain WHY, not just WHAT — the agent is smart and responds to reasoning
- Keep under 500 lines; use references/ for overflow
- Include examples with realistic inputs and outputs
- Avoid heavy-handed MUSTs; prefer explaining the reasoning
- For large reference files (>300 lines), include a table of contents in the reference

### Write Reference Files (if needed)

Place in `{skill-name}/references/`. These are loaded on-demand when the skill references them.

**When to create reference files:**
- Domain-specific documentation (API specs, schema definitions)
- Multi-variant support (e.g., aws.md, gcp.md, azure.md)
- Large lookup tables or configuration references
- Style guides or formatting specifications

### Write Scripts (if needed)

Place in `{skill-name}/scripts/`. These execute without being loaded into context.

**When to create scripts:**
- Deterministic transformations (file format conversion, data extraction)
- Validation logic (schema checking, linting)
- Repetitive multi-step operations
- Tasks where code is more reliable than natural language instructions

**Script guidelines:**
- Include a docstring explaining usage
- Accept command-line arguments for flexibility
- Handle errors gracefully with clear messages
- Use standard libraries where possible

### Write Companion Artifacts (if needed)

**Steering files** → Place in `.kiro/steering/`
```yaml
---
inclusion: {always|fileMatch|manual}
fileMatchPattern: "{pattern}"  # only for fileMatch
---
# {Title}
{content}
```

**Agent hooks** → Place in `.kiro/hooks/`
```json
{
  "name": "{Hook Name}",
  "version": "1.0.0",
  "description": "{what the hook does}",
  "when": {
    "type": "{eventType}",
    "patterns": ["{file patterns}"]
  },
  "then": {
    "type": "{askAgent|runCommand}",
    "prompt": "{prompt for askAgent}",
    "command": "{command for runCommand}"
  }
}
```

**Custom agents** → Define as markdown files with role, inputs, process, and output format.

### Write the Decision Log

Save the decision log as `{skill-name}/DECISION_LOG.md` so it persists with the skill for future reference.

---

## A5: Validate and Present

### Structure Checks
- [ ] SKILL.md exists and has valid YAML frontmatter
- [ ] `name` field is kebab-case, max 64 characters
- [ ] `description` field is present and under 1024 characters
- [ ] No unexpected keys in frontmatter (allowed: name, description, license, allowed-tools, metadata, compatibility)
- [ ] SKILL.md body is under 500 lines (or has clear pointers to references)
- [ ] All referenced files exist (scripts, references, assets)

### Content Checks
- [ ] Description includes trigger contexts (is "pushy")
- [ ] Instructions use imperative form
- [ ] Examples are realistic and complete
- [ ] Edge cases are addressed
- [ ] Scripts have docstrings and error handling

### Companion Artifact Checks
- [ ] Steering files have valid frontmatter with inclusion mode
- [ ] Hook JSON follows the required schema (name, version, when, then)
- [ ] Custom agent markdown files define role, inputs, process, output

### Present to User

Show the complete output with the decision log rationale, then invite changes:

```
Skill created: {skill-name}/
├── SKILL.md ({line count} lines)
├── references/{files}
├── scripts/{files}
├── assets/{files}
└── DECISION_LOG.md

Companion artifacts:
├── .kiro/steering/{files}
├── .kiro/hooks/{files}
└── .kiro/agents/{files}
```

**Decision summary:** {2-3 sentence recap of the architecture rationale}

> Everything is in place. Take a look and let me know if you'd like any changes — I can adjust the structure, rewrite sections, add or remove files, or rework the approach entirely.

---

# Workflow B: Update an Existing Skill

## B1: Understand the Current Skill

1. Read the SKILL.md file completely
2. Note the frontmatter fields (name, description, etc.)
3. Understand the skill's purpose and workflow
4. List all bundled resources (references/, scripts/, assets/)
5. Read key reference files and scripts to understand dependencies
6. Check for companion artifacts in `.kiro/steering/`, `.kiro/hooks/`, `.kiro/agents/`

---

## B2: Capture Change Intent

**Common change types:**
- **Add capability** — New feature or workflow step
- **Fix behavior** — Something isn't working as expected
- **Improve quality** — Better output, clearer instructions
- **Refactor structure** — Reorganize files, extract scripts
- **Update triggers** — Change when the skill activates
- **Add companions** — New steering, hooks, or agents

**Gather:**
1. What specific change is needed?
2. Why is this change needed?
3. Are there examples of current behavior vs desired behavior?
4. Should any existing behavior be preserved unchanged?

---

## B3: Change Impact Analysis

### Identify Affected Files

| File | Change Type | Description |
|------|-------------|-------------|
| SKILL.md | Modify | {what changes} |
| references/x.md | Add/Modify/Remove | {what changes} |
| scripts/y.py | Add/Modify/Remove | {what changes} |

### Assess Risk

- **Breaking changes** — Will this change how the skill triggers or alter expected output format?
- **Side effects** — Could this affect companion artifacts or other skills?
- **Reversibility** — Can this change be easily undone?

### Preservation Rules

- **Always preserve the skill name** — Never change the `name` frontmatter field unless explicitly asked
- **Preserve working behavior** — Don't break things that currently work
- **Preserve the description's trigger scope** — Only narrow or widen triggers if requested

---

## B4: Implement Changes

Apply the changes directly. No confirmation gate — run to completion.

### Guidelines

- Make surgical edits — change only what's needed
- Keep the skill's voice and style consistent
- If adding new sections to SKILL.md, place them logically within the existing structure
- If the skill is approaching 500 lines, consider extracting content to references/
- Update any companion artifacts that are affected
- If adding scripts, follow the existing script patterns in the skill

### Update Decision Log

Append to the existing DECISION_LOG.md (or create one):

```markdown
## Update: {date} — {change summary}

### Change Intent
{What the user wants to change and why}

### Changes Made
{List of specific changes with rationale}

### Impact Analysis
- Breaking changes: {yes/no, details}
- Files modified: {list}
- Files added: {list}
- Files removed: {list}

### Rationale
{Why these specific changes address the user's needs}
```

---

## B5: Validate and Present

Run the same validation checks as Workflow A, Phase A5. Then present:

```
Skill updated: {skill-name}/
Changes:
  Modified: {files}
  Added: {files}
  Removed: {files}

Decision log updated: DECISION_LOG.md
```

> Here's what changed. Let me know if you'd like any adjustments.

---

# Workflow C: Convert Prompts to Skills

## C1: Identify Source Material

### Source Types

**Q Developer Prompts:**
- `.md` or `.txt` files containing prompt templates
- Rules files with coding standards or conventions
- Project-level instruction files
- Custom prompt libraries

**Other Sources:**
- GitHub Copilot instructions (`.github/copilot-instructions.md`)
- Cursor rules (`.cursorrules`)
- Aider conventions (`.aider.conf.yml`)
- Claude project instructions
- Custom system prompts or instruction sets
- Team wikis or runbooks

### Gather Source Files

Ask the user to provide:
1. The source file(s) or paste the content
2. Context about how these prompts are currently used
3. Which prompts are most important or frequently used
4. Whether they want a single skill or multiple skills

---

## C2: Analyze and Classify

For each piece of source content, classify it:

| Content | Type | Best Target |
|---------|------|-------------|
| Task-specific workflow instructions | Procedural | **Skill** |
| Coding standards and conventions | Persistent rules | **Steering (always)** |
| Language-specific rules | Conditional rules | **Steering (fileMatch)** |
| One-off reference material | On-demand | **Steering (manual)** or **Skill reference** |
| Event-triggered automation | Reactive | **Hook** |
| Specialized sub-task instructions | Delegated | **Custom agent** |

### Mapping Rules

**Convert to Skill when:**
- The content describes a specific task or workflow
- It has clear trigger conditions (when to use it)
- It produces a specific output
- It benefits from bundled scripts or references

**Convert to Steering when:**
- The content is about standards, conventions, or rules
- It should apply broadly across interactions (always inclusion)
- It should apply when specific file types are in context (fileMatch)
- It's reference material the user wants available on demand (manual)

**Convert to Hook when:**
- The content describes an action that should happen automatically
- It's triggered by file changes, tool use, or other IDE events

**Convert to Custom Agent when:**
- The content describes a specialized role for a sub-task
- It needs isolated context and specific instructions

### Identify Conversion Challenges

Flag content that doesn't map cleanly:
- Prompts that assume a different tool's capabilities
- Rules that reference features not available in Kiro
- Content that mixes multiple concerns (split it)
- Overly vague instructions that need sharpening

---

## C3: Produce Conversion Plan and Decision Log

### Conversion Map

```markdown
## Conversion Plan

### Source: {source file/description}

| Source Section | Target Artifact | Target Path | Notes |
|---------------|-----------------|-------------|-------|
| {section 1} | Skill | {skill-name}/SKILL.md | {notes} |
| {section 2} | Steering | .kiro/steering/{name}.md | {notes} |
| {section 3} | Hook | .kiro/hooks/{name}.json | {notes} |
| {section 4} | Dropped | — | {reason for dropping} |
```

### Transformation Notes

For each conversion, note what changes are needed:
- **Reframing** — How instructions need to be rewritten for Kiro's context
- **Splitting** — Content that needs to be separated into multiple artifacts
- **Merging** — Related content that should be combined
- **Enhancing** — Areas where the original is too vague and needs detail
- **Dropping** — Content that doesn't apply to Kiro (explain why)

### Decision Log

```markdown
## Decision Log: Conversion of {source description}

### Source Analysis
{Summary of what was analyzed}

### Conversion Strategy
{Overall approach — single skill vs multiple, what goes where}

### Rationale
- {Reason 1}
- {Reason 2}

### Content Dropped
- {Item 1}: {reason}

### Enhancements Made
- {Enhancement 1}: {reason}
```

---

## C4: Implement Conversion

### Convert to Skills

For each skill, follow the implementation steps from Workflow A, Phase A4.

**Key conversion guidelines:**
- Rewrite instructions in imperative form for Kiro's agent
- Add a "pushy" description with trigger contexts
- Extract reusable logic into scripts/
- Move large reference material into references/
- Add examples if the source didn't have them
- Keep SKILL.md under 500 lines

**Q Developer specific conversions:**
- Q Developer "rules" → Kiro steering files (persistent context, not task-specific)
- Q Developer "prompts" with specific tasks → Kiro skills
- Q Developer project-level instructions → Kiro steering (always inclusion)
- Q Developer language-specific rules → Kiro steering (fileMatch inclusion)

### Convert to Steering

```yaml
---
inclusion: {always|fileMatch|manual}
fileMatchPattern: "{pattern}"  # only for fileMatch
---
# {Title}

{Converted content, rewritten for Kiro's steering format}
```

**Conversion guidelines:**
- Rewrite rules to be clear and actionable
- Remove references to other tools (Q Developer, Copilot, etc.)
- Add context about when and why each rule matters
- Group related rules logically

### Convert to Hooks

```json
{
  "name": "{Hook Name}",
  "version": "1.0.0",
  "description": "{what the hook does}",
  "when": { "type": "{eventType}", "patterns": ["{patterns}"] },
  "then": { "type": "{askAgent|runCommand}", "prompt": "{prompt}", "command": "{command}" }
}
```

### Convert to Custom Agents

Create markdown files defining role, inputs, process, and output format.

---

## C5: Validate and Present

Run validation checks for each artifact type (see Validation Checklists below). Then present:

```markdown
## Conversion Complete

### Source
{source description}

### Artifacts Created

**Skills:**
- {skill-name}/ — {description}

**Steering:**
- .kiro/steering/{name}.md — {description} ({inclusion mode})

**Hooks:**
- .kiro/hooks/{name}.json — {description}

**Custom Agents:**
- {path} — {description}

### Content Not Converted
- {item}: {reason}

### Decision Log
Saved to: {skill-name}/DECISION_LOG.md
```

> Conversion complete. Let me know if you'd like to adjust any of the artifacts, change the mapping, or iterate on specific pieces.

---

# Workflow D: Create Steering, Hooks, or Custom Agents

Use this workflow when creating these artifacts standalone (not as part of a skill).

## Steering Files

### When to Create

- Coding standards or conventions the agent should always follow
- Language-specific rules that apply when certain files are in context
- Reference material that should be available on demand
- Project-level context that influences agent behavior

### Inclusion Modes

| Mode | Frontmatter | When Loaded | Use Case |
|------|-------------|-------------|----------|
| Always | `inclusion: auto` (or no frontmatter) | Every interaction | Team standards, project conventions |
| Conditional | `inclusion: fileMatch` + `fileMatchPattern` | When matching files are in context | Language-specific rules, framework patterns |
| Manual | `inclusion: manual` | User provides via `#` in chat | Reference material, specialized guides |

### Implementation

Determine the need, then implement directly:

**Always-included steering:**
```yaml
---
inclusion: auto
---
# {Title}

{Content — rules, standards, conventions}
```

**Conditional steering (file-match):**
```yaml
---
inclusion: fileMatch
fileMatchPattern: "*.ts"
---
# TypeScript Standards

{Content — TypeScript-specific rules}
```

**Manual steering:**
```yaml
---
inclusion: manual
---
# {Title}

{Content — reference material available on demand}
```

**File references in steering:**
```markdown
See #[[file:openapi.yaml]] for the API specification.
```

**Location:** `.kiro/steering/` (workspace) or `~/.kiro/steering/` (user-level)

### Validate

- [ ] Frontmatter is valid YAML
- [ ] Inclusion mode is correctly set
- [ ] fileMatchPattern is valid (for fileMatch mode)
- [ ] Content is clear and actionable
- [ ] File is in the correct location

---

## Agent Hooks

### When to Create

- Automatic linting or formatting on file save
- Agent review of changes before or after tool use
- Commands to run when files are created or deleted
- Automated checks before or after spec task execution

### Event Types Reference

| Event | Trigger | Requires |
|-------|---------|----------|
| `fileEdited` | User saves a file | `patterns` |
| `fileCreated` | User creates a file | `patterns` |
| `fileDeleted` | User deletes a file | `patterns` |
| `userTriggered` | User manually triggers | — |
| `promptSubmit` | Message sent to agent | — |
| `agentStop` | Agent execution completes | — |
| `preToolUse` | Before a tool executes | `toolTypes` |
| `postToolUse` | After a tool executes | `toolTypes` |
| `preTaskExecution` | Before spec task starts | — |
| `postTaskExecution` | After spec task completes | — |

### Tool Types for preToolUse / postToolUse

| Category | Matches |
|----------|---------|
| `read` | File reading tools |
| `write` | File writing tools |
| `shell` | Terminal/command tools |
| `web` | Web search/fetch tools |
| `spec` | Spec-related tools |
| `*` | All tools |
| `.*regex.*` | Custom regex pattern for MCP tool names |

### Implementation

Use the `createHook` tool or write JSON directly to `.kiro/hooks/`.

**Example hooks:**

**Lint on save:**
```json
{
  "name": "Lint on Save",
  "version": "1.0.0",
  "description": "Run ESLint when TypeScript files are saved",
  "when": { "type": "fileEdited", "patterns": ["*.ts", "*.tsx"] },
  "then": { "type": "runCommand", "command": "npx eslint --fix" }
}
```

**Review write operations:**
```json
{
  "name": "Review Writes",
  "version": "1.0.0",
  "description": "Verify write operations follow coding standards",
  "when": { "type": "preToolUse", "toolTypes": ["write"] },
  "then": { "type": "askAgent", "prompt": "Before writing, verify this change follows our project coding standards and conventions." }
}
```

**Run tests after task:**
```json
{
  "name": "Post-Task Tests",
  "version": "1.0.0",
  "description": "Run test suite after completing a spec task",
  "when": { "type": "postTaskExecution" },
  "then": { "type": "runCommand", "command": "npm run test" }
}
```

### Validate

- [ ] JSON is valid
- [ ] Required fields present (name, version, when.type, then.type)
- [ ] Event type is valid
- [ ] patterns provided for file events
- [ ] toolTypes provided for tool events
- [ ] prompt provided for askAgent actions
- [ ] command provided for runCommand actions
- [ ] No circular dependency risk (preToolUse hooks that trigger themselves)

---

## Custom Agents

### When to Create

- A skill needs to delegate complex sub-tasks
- Different parts of a workflow need isolated context
- You want specialized roles (reviewer, analyzer, generator)
- A task benefits from parallel execution with different instructions

### Implementation

```markdown
# {Agent Name}

{Brief description of the agent's role}

## Role

{Detailed description of what this agent does and its expertise}

## Inputs

You receive these parameters:
- **{param1}**: {description}
- **{param2}**: {description}

## Process

### Step 1: {Step Name}
{Detailed instructions}

### Step 2: {Step Name}
{Detailed instructions}

## Output Format

{Exact format the agent should produce, with JSON schema if applicable}
```

### Validate

- [ ] Role is clearly defined
- [ ] All inputs are documented
- [ ] Process steps are actionable
- [ ] Output format is specified with examples
- [ ] Agent doesn't overlap with existing agents

---

## Combining Artifacts

When creating multiple artifact types together, follow this order:

1. **Steering files first** — They provide context that skills and hooks may reference
2. **Skills second** — They may reference steering files and define when hooks are useful
3. **Custom agents third** — They support skills with specialized sub-tasks
4. **Hooks last** — They automate workflows defined by skills and steering

Always produce a combined decision log explaining how the artifacts work together.

Present everything at the end and invite changes.

---

# Schemas and Templates

## SKILL.md Frontmatter

```yaml
---
name: skill-name                    # Required. Kebab-case, max 64 chars.
description: >                      # Required. Max 1024 chars. Primary trigger mechanism.
  What the skill does and when to use it.
  Include specific trigger contexts.
license: MIT                        # Optional. License identifier.
allowed-tools:                      # Optional. Tools the skill may use.
  - tool_name
metadata:                           # Optional. Additional metadata.
  key: value
compatibility:                      # Optional. Dependencies and requirements.
  - requirement
---
```

**Allowed frontmatter properties:** name, description, license, allowed-tools, metadata, compatibility. Any other properties cause validation failure.

**Naming rules:** Kebab-case only, max 64 characters, no leading/trailing/consecutive hyphens, lowercase letters + numbers + hyphens only.

**Description rules:** Max 1024 characters, no angle brackets, should be "pushy" with trigger contexts.

## Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── DECISION_LOG.md       # Recommended
├── references/           # Optional — docs loaded on demand
├── scripts/              # Optional — executable code
└── assets/               # Optional — templates, icons, fonts
```

| Directory | Purpose | Loading |
|-----------|---------|---------|
| `references/` | Documentation loaded into context on demand | Agent reads when referenced |
| `scripts/` | Executable code for deterministic tasks | Agent executes without loading into context |
| `assets/` | Files used in output (templates, icons) | Agent uses as-is |

## Steering File Frontmatter

```yaml
---
inclusion: auto          # auto (default), fileMatch, or manual
fileMatchPattern: "*.ts" # Required only for fileMatch
---
```

**File reference syntax:** `#[[file:path/to/file.yaml]]`

**Location:** `.kiro/steering/*.md` (workspace) or `~/.kiro/steering/*.md` (user-level)

## Hook Schema

```json
{
  "name": "string (required)",
  "version": "string (required)",
  "description": "string (optional)",
  "when": {
    "type": "eventType (required)",
    "patterns": ["file patterns (for file events)"],
    "toolTypes": ["tool categories or regex (for tool events)"]
  },
  "then": {
    "type": "askAgent or runCommand (required)",
    "prompt": "string (for askAgent)",
    "command": "string (for runCommand)"
  }
}
```

**Location:** `.kiro/hooks/*.json`

## Custom Agent Template

```markdown
# {Agent Name}

{One-line description.}

## Role
{Detailed description of expertise and constraints.}

## Inputs
- **{param1}**: {type} — {description}
- **{param2}**: {type} — {description}

## Process
### Step 1: {Name}
{Instructions}

### Step 2: {Name}
{Instructions}

## Output Format
{JSON schema or format specification}

## Guidelines
- {Guideline 1}
- {Guideline 2}
```

## Decision Log Template

```markdown
## Decision Log: {artifact-name}

**Date:** {YYYY-MM-DD}

### Intent
{What the user wants to accomplish}

### Architecture Chosen
| Artifact | Path | Purpose |
|----------|------|---------|
| {type} | {path} | {purpose} |

### Rationale
- {Reason 1}
- {Reason 2}

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| {Alt 1} | {reason} |

### Trade-offs
- {Trade-off 1}
- {Trade-off 2}
```

## Q Developer to Kiro Mapping

| Q Developer Concept | Kiro Equivalent | Notes |
|---------------------|-----------------|-------|
| Prompt template | Skill (SKILL.md) | Task-specific workflows |
| Rules file | Steering (always) | Persistent coding standards |
| Language rules | Steering (fileMatch) | Conditional on file type |
| Project instructions | Steering (always) | Project-level context |
| Custom commands | Skill + scripts/ | Executable workflows |
| Inline suggestions | Steering (fileMatch) | Context-aware guidance |

## Progressive Disclosure

| Level | What | Size Guidance | When Loaded |
|-------|------|---------------|-------------|
| 1. Metadata | name + description | ~100 words | Always in context |
| 2. SKILL.md body | Instructions, examples | <500 lines | When skill triggers |
| 3. Bundled resources | Scripts, references, assets | Unlimited | On demand |

---

# Validation Checklists

## Skill Validation
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name` is kebab-case, max 64 chars
- [ ] `description` is present, max 1024 chars, no angle brackets
- [ ] No unexpected frontmatter keys
- [ ] Body under 500 lines (or has clear pointers to references)
- [ ] All referenced files exist
- [ ] Description includes trigger contexts (is "pushy")
- [ ] Instructions use imperative form
- [ ] Examples are realistic and complete
- [ ] Scripts have docstrings and error handling

## Steering Validation
- [ ] Valid YAML frontmatter (if present)
- [ ] Inclusion mode is valid (auto, fileMatch, manual)
- [ ] fileMatchPattern present for fileMatch mode
- [ ] Content is clear and actionable
- [ ] File references use correct syntax

## Hook Validation
- [ ] Valid JSON
- [ ] `name` and `version` present
- [ ] `when.type` is a valid event type
- [ ] `patterns` present for file events
- [ ] `toolTypes` present for tool events
- [ ] `then.type` is `askAgent` or `runCommand`
- [ ] `prompt` present for askAgent / `command` present for runCommand
- [ ] No circular dependency risk

## Custom Agent Validation
- [ ] Role clearly defined
- [ ] All inputs documented with types
- [ ] Process steps are actionable
- [ ] Output format specified with examples
- [ ] No overlap with existing agents
