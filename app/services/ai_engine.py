import json
import redis.asyncio as redis
from sentence_transformers import SentenceTransformer
from app.core.config import settings # Assume settings has REDIS_URL

class AIEngine:
    def __init__(self):
        # Using a lightweight, high-performance model (384 dimensions)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Async Redis client for non-blocking I/O
        self.cache = redis.from_url("redis://redis:6379", decode_responses=True)

    async def get_embedding(self, text: str) -> list[float]:
        """
        Satisfies: 'Reduced redundant AI model calls by 30% using Redis caching'
        """
        cache_key = f"embed:{text}"
        
        # 1. Check Cache
        cached_vector = await self.cache.get(cache_key)
        if cached_vector:
            return json.loads(cached_vector)

        # 2. If not in cache, generate (This is the AI model call)
        # Note: We run this in a threadpool because model.encode is CPU bound
        import asyncio
        loop = asyncio.get_event_loop()
        vector = await loop.run_in_executor(None, self.model.encode, text)
        vector_list = vector.tolist()

        # 3. Store in cache for 24 hours to save future costs
        await self.cache.setex(cache_key, 86400, json.dumps(vector_list))
        
        return vector_list