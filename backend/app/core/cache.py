import hashlib
import json
from typing import Any

from redis.asyncio import Redis

from app.core.config import Settings


class CacheClient:
    def __init__(self, settings: Settings):
        self._ttl = settings.cache_ttl_seconds
        self._redis: Redis | None = None
        self._memory_cache: dict[str, str] = {}
        if settings.redis_url:
            self._redis = Redis.from_url(settings.redis_url, decode_responses=True)

    @staticmethod
    def _key(namespace: str, payload: dict[str, Any]) -> str:
        normalized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        return f"vedra:{namespace}:{digest}"

    async def get_json(self, namespace: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        key = self._key(namespace, payload)
        raw = None
        if self._redis:
            raw = await self._redis.get(key)
        else:
            raw = self._memory_cache.get(key)
        return json.loads(raw) if raw else None

    async def set_json(self, namespace: str, payload: dict[str, Any], value: dict[str, Any]) -> None:
        key = self._key(namespace, payload)
        serialized = json.dumps(value, ensure_ascii=False)
        if self._redis:
            await self._redis.set(key, serialized, ex=self._ttl)
        else:
            self._memory_cache[key] = serialized
