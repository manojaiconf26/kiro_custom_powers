# Code Reviewer Agent

An AI-powered code review agent built with the [Strands Agents SDK](https://strandsagents.com). It reads your code, inspects git diffs, and produces structured review reports with actionable feedback.

## Providers

| Provider | Use Case | Model |
|----------|----------|-------|
| **Ollama** | Local development (default) | `qwen2.5-coder:14b` |
| **Groq** | Local dev with cloud inference | `llama-3.3-70b-versatile` |
| **Bedrock** | Production / deployed | `anthropic.claude-sonnet-4-20250514-v1:0` |

## Quick Start

### 1. Install

```bash
cd code-reviewer-agent
pip install -e .
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your provider settings
```

### 3. Run

```bash
# Review last commit (Ollama, default)
code-reviewer

# Review with Groq
code-reviewer --provider groq

# Review staged changes
code-reviewer --staged

# Review specific files
code-reviewer --files src/app.py src/utils.py

# Diff against a branch
code-reviewer --diff main

# Interactive chat mode
code-reviewer --interactive
```

## Provider Setup

### Ollama (Local)

```bash
# Install Ollama: https://ollama.ai
ollama pull qwen2.5-coder:14b
ollama serve
```

Any Ollama model with tool-calling support works. Good choices:
- `qwen2.5-coder:14b` — strong at code tasks
- `llama3.1` — general purpose
- `mistral` — fast and capable

### Groq (Cloud)

1. Get an API key at [console.groq.com/keys](https://console.groq.com/keys)
2. Set `GROQ_API_KEY` in your `.env`
3. Run with `--provider groq`

### Amazon Bedrock (Production)

1. Configure AWS credentials (`aws configure` or IAM role)
2. Enable model access in the [Bedrock console](https://console.aws.amazon.com/bedrock)
3. Run with `--provider bedrock`

## Custom Guidelines

The agent ships with general best practices, but you can layer on your team's specific
standards. Create a `.code-review-guidelines.md` file in your project root:

```bash
cp .code-review-guidelines.example.md /path/to/your/project/.code-review-guidelines.md
# Edit the file with your team's rules
```

The agent auto-discovers this file from:
1. The current working directory
2. The git repository root

Or pass it explicitly:

```bash
code-reviewer --guidelines /path/to/my-team-standards.md
```

Custom guidelines are injected into the system prompt at **highest priority** — when
they conflict with the general criteria, your team's rules win. Violations are flagged
as Critical or Improvements depending on severity.

See [`.code-review-guidelines.example.md`](.code-review-guidelines.example.md) for a
full template covering language standards, architecture rules, security policies, and
testing requirements.

## Tools

The agent has access to these tools:

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `list_files` | List project files with optional glob filtering |
| `get_git_diff` | Get diff against a git ref |
| `get_git_staged_diff` | Get diff of staged changes |
| `search_in_files` | Regex search across files |
| `write_review_report` | Save the review report to a file |

## Output

The agent produces a structured markdown report (`REVIEW.md` by default):

```markdown
# Code Review Report

## Summary
Overview of changes and assessment.

## Findings

### Critical
Bugs, security issues, data loss risks.

### Improvements
Recommended changes for better code quality.

### Nitpicks
Minor style suggestions.

## Positive Highlights
Things done well.
```

## Project Structure

```
code-reviewer-agent/
├── pyproject.toml                          # Project config and dependencies
├── .env.example                            # Environment variable template
├── .code-review-guidelines.example.md      # Sample custom guidelines template
├── README.md
└── code_reviewer/
    ├── __init__.py
    ├── agent.py                            # Agent construction
    ├── guidelines.py                       # Custom guidelines loader
    ├── main.py                             # CLI entry point
    ├── prompts.py                          # System prompt builder
    ├── providers.py                        # Model provider factory
    └── tools.py                            # Custom review tools
```
