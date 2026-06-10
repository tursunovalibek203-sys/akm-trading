import redis.asyncio as aioredis
from app.core.config import settings
from app.core.redis_mock import InMemoryRedis

_redis_client: aioredis.Redis | InMemoryRedis | None = None
_use_mock = False


async def get_redis() -> aioredis.Redis | InMemoryRedis:
    global _redis_client, _use_mock

    if _redis_client is not None:
        return _redis_client

    # localhost yoki mock rejimida — real ulanishsiz ishlaydi
    is_local = settings.REDIS_URL.startswith("redis://localhost") or \
               settings.REDIS_URL.startswith("redis://127.0.0.1")

    if is_local:
        _redis_client = InMemoryRedis()
        _use_mock = True
        return _redis_client

    # Cloud Redis (Upstash va boshqalar)
    try:
        client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=3,
        )
        await client.ping()
        _redis_client = client
    except Exception:
        # Ulanish muvaffaqiyatsiz — in-memory ga tushadi
        _redis_client = InMemoryRedis()
        _use_mock = True

    return _redis_client


async def close_redis() -> None:
    global _redis_client, _use_mock
    if _redis_client and not _use_mock:
        await _redis_client.aclose()
    _redis_client = None
    _use_mock = False
