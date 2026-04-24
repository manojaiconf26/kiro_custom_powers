"""Load enterprise-specific review guidelines from external files.

Guidelines are plain markdown files that describe your team's coding standards,
architecture patterns, naming conventions, security policies, etc. They get
injected into the agent's system prompt so the reviewer enforces your rules
alongside the general best practices.

Supported sources (checked in order):
  1. Explicit path via --guidelines CLI flag or guidelines_path argument
  2. .code-review-guidelines.md in the current working directory
  3. .code-review-guidelines.md in the repo root (git-based detection)

The file format is freeform markdown. Example:

    # Team Guidelines
    ## Naming
    - Use snake_case for Python, camelCase for TypeScript.
    ## Security
    - Never log PII fields. Use the `sanitize()` helper.
    ## Architecture
    - All API handlers must go through the middleware chain.
"""

import os
import subprocess


# Default filenames to search for (in priority order)
_DEFAULT_FILENAMES = [
    ".code-review-guidelines.md",
    "code-review-guidelines.md",
    "REVIEW_GUIDELINES.md",
]


def load_guidelines(path: str | None = None) -> str | None:
    """Load custom review guidelines from a file.

    Args:
        path: Explicit path to a guidelines file. If None, searches
              default locations automatically.

    Returns:
        The guidelines content as a string, or None if no file was found.
    """
    if path:
        return _read_file(path)

    # Search default locations
    for candidate in _candidate_paths():
        content = _read_file(candidate)
        if content is not None:
            return content

    return None


def _candidate_paths() -> list[str]:
    """Generate candidate file paths to check for guidelines."""
    candidates = []

    # Current working directory
    cwd = os.getcwd()
    for name in _DEFAULT_FILENAMES:
        candidates.append(os.path.join(cwd, name))

    # Git repo root (if different from cwd)
    repo_root = _git_repo_root()
    if repo_root and os.path.abspath(repo_root) != os.path.abspath(cwd):
        for name in _DEFAULT_FILENAMES:
            candidates.append(os.path.join(repo_root, name))

    return candidates


def _git_repo_root() -> str | None:
    """Detect the git repository root, or None if not in a repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _read_file(path: str) -> str | None:
    """Read a file and return its content, or None if it doesn't exist."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except (OSError, UnicodeDecodeError):
        return None
