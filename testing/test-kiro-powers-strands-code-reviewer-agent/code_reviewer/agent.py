"""Code reviewer agent construction."""

from strands import Agent

from .guidelines import load_guidelines
from .prompts import build_system_prompt
from .providers import get_model
from .tools import (
    get_git_diff,
    get_git_staged_diff,
    list_files,
    read_file,
    search_in_files,
    write_review_report,
)

TOOLS = [
    read_file,
    list_files,
    get_git_diff,
    get_git_staged_diff,
    search_in_files,
    write_review_report,
]


def build_agent(
    provider: str | None = None,
    guidelines_path: str | None = None,
) -> Agent:
    """Build and return a code reviewer agent.

    Args:
        provider: Model provider to use ("ollama", "groq", or "bedrock").
                  Defaults to MODEL_PROVIDER env var, then "ollama".
        guidelines_path: Explicit path to a custom guidelines markdown file.
                         If None, auto-discovers from default locations.
    """
    model = get_model(provider)

    # Load custom guidelines (explicit path → auto-discovery → None)
    custom_guidelines = load_guidelines(guidelines_path)
    system_prompt = build_system_prompt(custom_guidelines)

    if custom_guidelines:
        print("📏 Custom guidelines loaded.")

    agent = Agent(
        model=model,
        tools=TOOLS,
        system_prompt=system_prompt,
    )

    return agent
