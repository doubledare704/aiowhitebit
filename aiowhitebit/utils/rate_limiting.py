"""Rate limiting utilities for the WhiteBit API."""
import time
import asyncio
from functools import wraps
from collections import deque

class RateLimiter:
    def __init__(self, limit: int, window: float):
        self.limit = limit
        self.window = window
        self.requests: deque = deque()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            
            # Remove expired timestamps
            while self.requests and self.requests[0] <= now - self.window:
                self.requests.popleft()
            
            if len(self.requests) >= self.limit:
                sleep_time = self.requests[0] - (now - self.window)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            
            self.requests.append(now)

def rate_limit(limit: int, window: float = 10.0):
    limiter = RateLimiter(limit, window)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await limiter.acquire()
            return await func(*args, **kwargs)
        return wrapper
    return decorator