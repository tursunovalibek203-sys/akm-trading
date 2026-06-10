"""
In-memory Redis mock — local dev uchun real Redis o'rniga ishlatiladi.
Faqat loyiha ishlatadigan metodlar implementatsiya qilingan.
"""
import asyncio
import time
from typing import Optional


class InMemoryRedis:
    def __init__(self) -> None:
        self._strings: dict[str, str] = {}
        self._expiry: dict[str, float] = {}
        self._lists: dict[str, list[str]] = {}

    def _clean(self, key: str) -> None:
        if key in self._expiry and time.time() > self._expiry[key]:
            self._strings.pop(key, None)
            self._expiry.pop(key, None)

    async def get(self, key: str) -> Optional[str]:
        self._clean(key)
        return self._strings.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> str:
        self._strings[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        return "OK"

    async def setex(self, key: str, seconds: int, value: str) -> str:
        self._strings[key] = value
        self._expiry[key] = time.time() + seconds
        return "OK"

    async def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            if key in self._strings:
                del self._strings[key]
                self._expiry.pop(key, None)
                removed += 1
            if key in self._lists:
                del self._lists[key]
                removed += 1
        return removed

    async def lpush(self, key: str, *values: str) -> int:
        if key not in self._lists:
            self._lists[key] = []
        for v in values:
            self._lists[key].insert(0, v)
        return len(self._lists[key])

    async def rpush(self, key: str, *values: str) -> int:
        if key not in self._lists:
            self._lists[key] = []
        for v in values:
            self._lists[key].append(v)
        return len(self._lists[key])

    async def lrange(self, key: str, start: int, stop: int) -> list[str]:
        lst = self._lists.get(key, [])
        end = None if stop == -1 else stop + 1
        return lst[start:end]

    async def ltrim(self, key: str, start: int, stop: int) -> str:
        lst = self._lists.get(key, [])
        end = None if stop == -1 else stop + 1
        self._lists[key] = lst[start:end]
        return "OK"

    async def brpop(self, key: str, timeout: int = 0) -> Optional[tuple[str, str]]:
        deadline = time.time() + timeout if timeout > 0 else None
        while True:
            lst = self._lists.get(key)
            if lst:
                value = lst.pop()
                return (key, value)
            if deadline is not None and time.time() >= deadline:
                return None
            await asyncio.sleep(0.05)

    async def ping(self) -> bool:
        return True

    async def aclose(self) -> None:
        pass
