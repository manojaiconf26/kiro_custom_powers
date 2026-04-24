"""Custom tools for the code reviewer agent."""

import os
import subprocess

from strands import tool


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a file and return them as a string.

    Args:
        file_path: Relative or absolute path to the file to read.
    """
    path = os.path.abspath(file_path)
    if not os.path.isfile(path):
        return f"Error: '{file_path}' does not exist or is not a file."
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"Error reading '{file_path}': {e}"


@tool
def list_files(directory: str = ".", pattern: str = "") -> str:
    """List files in a directory, optionally filtering by a glob pattern.

    Args:
        directory: Directory to list. Defaults to the current directory.
        pattern: Optional glob pattern to filter files (e.g. '*.py').
    """
    import glob

    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        return f"Error: '{directory}' is not a directory."

    if pattern:
        matches = glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        return "\n".join(sorted(matches)) or "No files matched the pattern."
    else:
        entries = []
        for root, dirs, files in os.walk(directory):
            # Skip hidden and common non-essential directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".venv")]
            for fname in sorted(files):
                entries.append(os.path.relpath(os.path.join(root, fname), directory))
        return "\n".join(entries[:500]) or "Directory is empty."


@tool
def get_git_diff(base_ref: str = "HEAD~1", path: str = ".") -> str:
    """Get the git diff for recent changes.

    Args:
        base_ref: Git ref to diff against. Defaults to 'HEAD~1' (last commit).
        path: Path scope for the diff. Defaults to the entire repo.
    """
    try:
        result = subprocess.run(
            ["git", "diff", base_ref, "--", path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            # Fall back to unstaged changes
            result = subprocess.run(
                ["git", "diff", "--", path],
                capture_output=True,
                text=True,
                timeout=30,
            )
        diff = result.stdout.strip()
        return diff if diff else "No diff found."
    except FileNotFoundError:
        return "Error: git is not installed or not in PATH."
    except subprocess.TimeoutExpired:
        return "Error: git diff timed out."
    except Exception as e:
        return f"Error running git diff: {e}"


@tool
def get_git_staged_diff() -> str:
    """Get the git diff for currently staged (added) changes, useful for pre-commit reviews."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        diff = result.stdout.strip()
        return diff if diff else "No staged changes found."
    except FileNotFoundError:
        return "Error: git is not installed or not in PATH."
    except Exception as e:
        return f"Error running git diff --cached: {e}"


@tool
def search_in_files(pattern: str, directory: str = ".", file_glob: str = "") -> str:
    """Search for a text pattern across files in a directory using grep-like matching.

    Args:
        pattern: The regex pattern to search for.
        directory: Root directory to search in. Defaults to current directory.
        file_glob: Optional file glob to restrict search (e.g. '*.py').
    """
    import re

    directory = os.path.abspath(directory)
    results = []
    count = 0
    max_results = 100

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".venv")]
        for fname in files:
            if file_glob and not _matches_glob(fname, file_glob):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8", errors="replace") as f:
                    for lineno, line in enumerate(f, 1):
                        if re.search(pattern, line):
                            rel = os.path.relpath(fpath, directory)
                            results.append(f"{rel}:{lineno}: {line.rstrip()}")
                            count += 1
                            if count >= max_results:
                                results.append(f"... truncated at {max_results} results")
                                return "\n".join(results)
            except (OSError, UnicodeDecodeError):
                continue

    return "\n".join(results) if results else "No matches found."


def _matches_glob(filename: str, glob_pattern: str) -> bool:
    """Simple glob matching for filenames."""
    import fnmatch
    return fnmatch.fnmatch(filename, glob_pattern)


@tool
def write_review_report(content: str, output_path: str = "REVIEW.md") -> str:
    """Write the final code review report to a markdown file.

    Args:
        content: The markdown-formatted review content to write.
        output_path: File path for the report. Defaults to 'REVIEW.md'.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Review report written to {output_path}"
    except Exception as e:
        return f"Error writing report: {e}"
