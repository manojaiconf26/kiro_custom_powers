"""CLI entry point for the code reviewer agent."""

import argparse
import os
import sys

from dotenv import load_dotenv


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="AI-powered code reviewer built with Strands Agents SDK",
    )
    parser.add_argument(
        "--provider",
        choices=["ollama", "groq", "bedrock"],
        default=os.getenv("MODEL_PROVIDER", "ollama"),
        help="Model provider to use (default: ollama)",
    )
    parser.add_argument(
        "--diff",
        default=None,
        help="Git ref to diff against (e.g. 'main', 'HEAD~3'). Defaults to HEAD~1.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Review only staged (git add) changes.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=None,
        help="Specific file(s) to review instead of a git diff.",
    )
    parser.add_argument(
        "--output",
        default="REVIEW.md",
        help="Output path for the review report (default: REVIEW.md)",
    )
    parser.add_argument(
        "--guidelines",
        default=None,
        help="Path to a custom guidelines markdown file. "
             "If omitted, auto-discovers .code-review-guidelines.md in cwd or repo root.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start an interactive chat session with the reviewer.",
    )

    args = parser.parse_args()

    # Import here so --help is fast even without deps installed
    from .agent import build_agent

    print(f"🔍 Code Reviewer Agent — provider: {args.provider}")
    print("-" * 50)

    agent = build_agent(provider=args.provider, guidelines_path=args.guidelines)

    if args.interactive:
        _interactive_mode(agent)
    else:
        _review_mode(agent, args)


def _review_mode(agent, args):
    """Run a one-shot code review."""
    if args.files:
        file_list = ", ".join(args.files)
        prompt = (
            f"Review the following files: {file_list}. "
            f"Read each file, analyze the code, and produce a review report. "
            f"Save the report to '{args.output}'."
        )
    elif args.staged:
        prompt = (
            "Review the currently staged git changes. "
            "Use get_git_staged_diff to see what changed, read relevant files for context, "
            f"and produce a review report. Save the report to '{args.output}'."
        )
    else:
        base_ref = args.diff or "HEAD~1"
        prompt = (
            f"Review the recent code changes by diffing against '{base_ref}'. "
            "Use get_git_diff to see what changed, read relevant files for full context, "
            f"and produce a review report. Save the report to '{args.output}'."
        )

    print(f"\n📋 Prompt: {prompt}\n")
    response = agent(prompt)
    print(f"\n{'=' * 50}")
    print(f"✅ Review complete. Report saved to {args.output}")


def _interactive_mode(agent):
    """Run an interactive chat loop with the reviewer."""
    print("💬 Interactive mode — type 'quit' or 'exit' to stop.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        agent(user_input)
        print()


if __name__ == "__main__":
    main()
