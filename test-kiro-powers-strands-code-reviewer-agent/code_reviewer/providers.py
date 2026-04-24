"""Model provider factory for the code reviewer agent.

Supports three providers:
  - ollama  : Local models via Ollama (default for local dev)
  - groq    : Groq cloud API (OpenAI-compatible, fast inference)
  - bedrock : Amazon Bedrock (production / deployed environments)
"""

import os


def get_model(provider: str | None = None):
    """Return a Strands model instance for the requested provider.

    Args:
        provider: One of "ollama", "groq", or "bedrock".
                  Falls back to the MODEL_PROVIDER env var, then "ollama".
    """
    provider = (provider or os.getenv("MODEL_PROVIDER", "ollama")).lower().strip()

    if provider == "ollama":
        return _build_ollama_model()
    elif provider == "groq":
        return _build_groq_model()
    elif provider == "bedrock":
        return _build_bedrock_model()
    else:
        raise ValueError(
            f"Unknown provider '{provider}'. Choose from: ollama, groq, bedrock"
        )


# ---------------------------------------------------------------------------
# Ollama — local models
# ---------------------------------------------------------------------------

def _build_ollama_model():
    from strands.models.ollama import OllamaModel

    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_id = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b")

    return OllamaModel(
        host=host,
        model_id=model_id,
        temperature=0.2,
    )


# ---------------------------------------------------------------------------
# Groq — OpenAI-compatible cloud API
# ---------------------------------------------------------------------------

def _build_groq_model():
    from strands.models.openai import OpenAIModel

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is required when using the groq provider. "
            "Get one at https://console.groq.com/keys"
        )

    model_id = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    return OpenAIModel(
        client_args={
            "api_key": api_key,
            "base_url": "https://api.groq.com/openai/v1",
        },
        model_id=model_id,
        params={
            "temperature": 0.2,
            "max_tokens": 4096,
        },
    )


# ---------------------------------------------------------------------------
# Amazon Bedrock — production / deployed
# ---------------------------------------------------------------------------

def _build_bedrock_model():
    from strands.models import BedrockModel

    model_id = os.getenv("BEDROCK_MODEL", "anthropic.claude-sonnet-4-20250514-v1:0")
    region = os.getenv("AWS_REGION", "us-east-1")

    return BedrockModel(
        model_id=model_id,
        region_name=region,
        temperature=0.2,
        max_tokens=4096,
    )
