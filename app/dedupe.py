import aioredis

class DeduplicationCache:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.ttl = 300  # 5 minutes

    async def is_duplicate(self, event_id: str) -> bool:
        exists = await self.redis.exists(event_id)
        if exists:
            return True
        await self.redis.set(event_id, "1", ex=self.ttl)
        return False