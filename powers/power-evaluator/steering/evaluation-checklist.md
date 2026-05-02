# Evaluation Checklist

This steering file contains the complete evaluation rubric and the step-by-step workflow for performing a power evaluation.

---

## Evaluation Workflow

Follow these steps in order when evaluating a power:

### Step 1: Identify the Power

Determine the power's location. This could be:
- A path in the workspace (e.g., `powers/my-power`)
- An installed power (activate it to read POWER.md)
- A Git repository URL (clone or fetch the files)

### Step 2: Read All Power Files

Read every file in the power directory:

1. **POWER.md** — Read the full file including frontmatter
2. **mcp.json** — Read if present (determines power type)
3. **steering/*.md** — Read all steering files
4. **.gitignore** — Check if present
5. **Any other files** — Note unexpected files

Record what you find:
- Power type: Guided MCP Power (has mcp.json) or Knowledge Base Power (no mcp.json)
- File inventory: List all files found
- Missing files: Note any expected files that are absent

### Step 3: Evaluate Each Dimension

Work through each dimension below, checking every criterion. Record your findings as you go.

### Step 4: Calculate Scores

Assign a score (1-4) for each dimension based on how many criteria are met.

### Step 5: Compile the Report

Produce the evaluation report in the format specified in POWER.md. Include:
- Summary with type, score, and rating
- Scorecard table
- Strengths (at least 2-3 things done well)
- Issues found (categorized as Critical, Warning, or Suggestion)
- Prioritized recommendations

---

## Dimension 1: Structure & Completeness

### Required Checks

**POWER.md Existence and Frontmatter:**
- [ ] POWER.md file exists in the power root directory
- [ ] Frontmatter block is present (delimited by `---`)
- [ ] `name` field is present and uses kebab-case (lowercase, hyphens)
- [ ] `displayName` field is present
- [ ] `description` field is present
- [ ] No invalid frontmatter fields are used (reject: version, tags, repository, license, or any field not in the valid set)
- [ ] Valid optional fields only: `keywords`, `author`

**Power Type Consistency:**
- [ ] If mcp.json exists → treat as Guided MCP Power
- [ ] If no mcp.json → treat as Knowledge Base Power
- [ ] No contradictions (e.g., POWER.md references MCP tools but no mcp.json exists)

**Directory Structure:**
- [ ] No unexpected top-level files (only POWER.md, mcp.json, .gitignore, steering/)
- [ ] If steering/ directory exists, it contains only .md files
- [ ] Steering files listed in POWER.md match actual files in steering/
- [ ] No empty steering files

**Scoring Guide:**
- **4 (Excellent):** All checks pass, clean structure
- **3 (Good):** Minor issues (e.g., missing .gitignore, one mismatched steering reference)
- **2 (Needs Work):** Missing optional but recommended elements, or structural inconsistencies
- **1 (Poor):** Missing POWER.md, invalid frontmatter, or broken structure

---

## Dimension 2: Documentation Quality

### Required Checks

**Overview Section:**
- [ ] Overview section exists
- [ ] Explains what the power does
- [ ] Explains why it's useful or what problem it solves
- [ ] Mentions key capabilities
- [ ] 2-3 paragraphs (not too short, not too long)

**Onboarding / Getting Started:**
- [ ] Onboarding, Quick Start, or Getting Started section exists
- [ ] Prerequisites listed (if any)
- [ ] Installation or setup steps provided (if applicable)
- [ ] Configuration steps documented (if applicable)

**Workflows / Usage:**
- [ ] At least one workflow or usage section exists
- [ ] Workflows have step-by-step instructions
- [ ] Steps are clear and actionable
- [ ] Workflows cover the primary use case of the power

**Code Examples:**
- [ ] Code examples are present (if applicable to the power type)
- [ ] Examples are complete (not snippets with `...` or `// TODO`)
- [ ] Examples use proper syntax highlighting (language specified in code blocks)
- [ ] Examples are realistic and runnable

**Troubleshooting:**
- [ ] Troubleshooting section exists
- [ ] At least 2-3 common problems documented
- [ ] Each problem has: symptoms, cause, and solution
- [ ] Solutions are actionable (not just "check the docs")

**Best Practices:**
- [ ] Best practices section exists
- [ ] At least 3-5 practices listed
- [ ] Practices are specific to this power's domain (not generic advice)

**General Quality:**
- [ ] No placeholder text (`{TODO}`, `TBD`, `FIXME`, `lorem ipsum`)
- [ ] No broken markdown (unclosed code blocks, malformed tables)
- [ ] Consistent heading hierarchy (no skipped levels)
- [ ] Reasonable document length (not too sparse, not bloated)

**Scoring Guide:**
- **4 (Excellent):** All sections present, high-quality content, complete examples
- **3 (Good):** Most sections present, content is useful, minor gaps
- **2 (Needs Work):** Missing important sections, thin content, incomplete examples
- **1 (Poor):** Minimal documentation, placeholder text, or largely unhelpful content

---

## Dimension 3: Usability & Agent Experience

### Required Checks

**Agent Workflow Clarity:**
- [ ] An agent reading POWER.md can understand what the power does without external context
- [ ] Workflows are structured so an agent can follow them step-by-step
- [ ] Instructions use imperative language ("Run this command", "Create this file")
- [ ] No ambiguous instructions ("you might want to", "consider doing")

**Steering File Organization:**
- [ ] If steering files exist, POWER.md lists them with descriptions
- [ ] Steering file descriptions accurately reflect their content
- [ ] Steering files cover distinct topics (no significant overlap)
- [ ] POWER.md provides enough context to know which steering file to read

**Content Sizing:**
- [ ] POWER.md is not bloated (under ~500 lines for powers with steering files)
- [ ] If POWER.md exceeds ~500 lines and has no steering files, consider whether it should be split
- [ ] Steering files are focused (each covers one topic or workflow)
- [ ] No single steering file is excessively long (over ~800 lines)

**Tool Documentation (Guided MCP Powers):**
- [ ] MCP tool names are mentioned accurately
- [ ] Tool parameters are documented (types, required vs optional)
- [ ] Tool usage examples show realistic scenarios
- [ ] Error handling guidance for tool failures

**Progressive Disclosure:**
- [ ] POWER.md provides a useful overview without needing to read steering files
- [ ] Steering files add depth, not duplicate POWER.md content
- [ ] A user can get started with just POWER.md

**Scoring Guide:**
- **4 (Excellent):** Agent can use the power effectively from documentation alone
- **3 (Good):** Mostly clear, minor ambiguities or missing tool details
- **2 (Needs Work):** Agent would struggle with some workflows, unclear guidance
- **1 (Poor):** Documentation is confusing, incomplete, or contradictory

---

## Dimension 4: Discoverability & Metadata

### Required Checks

**Name:**
- [ ] Uses kebab-case (lowercase with hyphens)
- [ ] Is descriptive (not too generic like "helper" or "utils")
- [ ] Is concise (ideally 1-3 words)
- [ ] Matches the directory name

**Display Name:**
- [ ] Uses Title Case
- [ ] Is 2-5 words
- [ ] Is clear and professional
- [ ] No emojis
- [ ] Accurately represents the power's purpose

**Description:**
- [ ] Maximum 3 sentences
- [ ] Focuses on value/capability (not implementation details)
- [ ] Uses active voice
- [ ] Is specific enough to differentiate from similar powers

**Keywords:**
- [ ] 5-7 keywords provided
- [ ] Keywords are specific to the power's domain
- [ ] No overly broad keywords ("test", "debug", "help", "api", "data")
- [ ] Keywords include variations users might search for
- [ ] Keywords don't overlap significantly with common Kiro features

**Scoring Guide:**
- **4 (Excellent):** All metadata is well-crafted, keywords are precise
- **3 (Good):** Metadata is solid, minor keyword improvements possible
- **2 (Needs Work):** Generic name/description, broad keywords, or missing keywords
- **1 (Poor):** Misleading metadata, no keywords, or very generic naming

---

## Dimension 5: MCP Configuration (Guided MCP Powers Only)

Skip this dimension entirely for Knowledge Base Powers.

### Required Checks

**Schema Validity:**
- [ ] mcp.json is valid JSON
- [ ] Top-level key is `mcpServers`
- [ ] Each server entry has either `command`/`args` (local) or `url` (remote), not both
- [ ] No unknown top-level keys in server entries

**Configuration Quality:**
- [ ] Server name is descriptive and consistent with the power name
- [ ] Environment variables are documented in POWER.md
- [ ] Required vs optional env vars are distinguished
- [ ] Default values noted where applicable

**Sharing Readiness:**
- [ ] Sensitive values use placeholders (API keys, paths, tokens)
- [ ] Placeholders are documented in POWER.md with instructions on how to obtain real values
- [ ] Or: no sensitive values needed (standard npm package)

**Tool Management:**
- [ ] If `disabledTools` is used, rationale is documented
- [ ] If `autoApprove` is used, it's limited to safe, read-only tools
- [ ] No tools are disabled without clear justification

**Scoring Guide:**
- **4 (Excellent):** Valid config, well-documented, sharing-ready
- **3 (Good):** Valid config, minor documentation gaps
- **2 (Needs Work):** Config works but poorly documented, or sharing issues
- **1 (Poor):** Invalid config, undocumented env vars, or hardcoded secrets

---

## Issue Severity Guide

When reporting issues, categorize them by severity:

### Critical
Issues that prevent the power from working correctly or violate required constraints.

Examples:
- Missing POWER.md
- Invalid frontmatter fields
- mcp.json with invalid JSON
- Missing required frontmatter fields (name, displayName, description)
- Steering files referenced in POWER.md but don't exist
- Hardcoded secrets in mcp.json

### Warning
Issues that degrade quality or usability but don't break the power.

Examples:
- Missing troubleshooting section
- Overly broad keywords
- Incomplete code examples
- Missing onboarding section
- POWER.md over 500 lines without steering files
- Placeholder text or TODO markers

### Suggestion
Improvements that would enhance the power but aren't required.

Examples:
- Could add more code examples
- Keywords could be more specific
- Description could be more concise
- Could add .gitignore
- Steering file descriptions could be more detailed
- Could add a best practices section

---

## Report Template

Use this template for the final evaluation report:

```markdown
# Power Evaluation: {power-name}

## Summary
- **Type:** Guided MCP Power | Knowledge Base Power
- **Location:** {path or source}
- **Overall Score:** X/20 (or X/16 for Knowledge Base)
- **Rating:** Excellent | Good | Needs Work | Poor

## Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Structure & Completeness | X/4 | {brief note} |
| Documentation Quality | X/4 | {brief note} |
| Usability & Agent Experience | X/4 | {brief note} |
| Discoverability & Metadata | X/4 | {brief note} |
| MCP Configuration | X/4 | {brief note or N/A} |
| **Total** | **X/20** | |

## Strengths
- {Specific thing done well}
- {Another strength}
- {Another strength}

## Issues Found

### Critical
- {Issue description and location}

### Warnings
- {Issue description and location}

### Suggestions
- {Improvement idea}

## Recommendations (Prioritized)
1. {Most important fix — what to change and why}
2. {Next priority}
3. {Next priority}
4. {Nice to have}
```
