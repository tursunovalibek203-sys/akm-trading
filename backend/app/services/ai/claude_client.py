"""
Claude API client — prompt caching bilan.
Multi-model: Haiku (pre-screen) → Sonnet (asosiy) → Opus (kritik).
"""
import anthropic
from app.core.config import settings
from app.core.logger import logger

# Bir marta yaratiladi — import paytida
_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY sozlanmagan — .env faylini tekshiring")
        _client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        logger.info("Claude API client tayyor")
    return _client


# ---------------------------------------------------------------
# Kichik yordamchi funksiyalar
# ---------------------------------------------------------------

def haiku_call(prompt: str, system: str = "") -> str:
    """Tez va arzon pre-screen uchun Haiku."""
    client = get_client()
    kwargs: dict = {
        "model": settings.ANTHROPIC_MODEL_HAIKU,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text if response.content else ""


def sonnet_call(
    messages: list[dict],
    system_blocks: list[dict],
    max_tokens: int = 2048,
) -> anthropic.types.Message:
    """
    Asosiy tahlil uchun Sonnet — prompt caching bilan.
    system_blocks: [{"type": "text", "text": "...", "cache_control": {...}}, ...]
    """
    client = get_client()
    return client.messages.create(
        model=settings.ANTHROPIC_MODEL_SONNET,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=messages,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
    )


def opus_call(
    messages: list[dict],
    system_blocks: list[dict],
    max_tokens: int = 2048,
) -> anthropic.types.Message:
    """Kritik qarorlar uchun Opus — adaptive thinking bilan."""
    client = get_client()
    return client.messages.create(
        model=settings.ANTHROPIC_MODEL_OPUS,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=messages,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
    )
