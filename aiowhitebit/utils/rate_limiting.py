"""Rate limiting utilities for the WhiteBit API."""

import asyncio
import time
from collections import deque
from functools import wraps


class RateLimiter:
    """Rate limiter for API requests.

    This class implements a token bucket algorithm for rate limiting API requests.
    It ensures that requests are made within the specified rate limits by tracking
    request timestamps and delaying requests when necessary.
    """

    def __init__(self, limit: int, window: float):
        """Initialize the rate limiter.

        Args:
            limit: Maximum number of requests allowed in the time window
            window: Time window in seconds
        """
        self.limit = limit
        self.window = window
        self.requests: deque = deque()
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Acquire a rate limit token.

        This method ensures that the rate limit is not exceeded by:
        1. Removing expired timestamps
        2. Waiting if the limit has been reached
        3. Adding the current timestamp to the queue
        """
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
    """Rate limiting decorator."""
    limiter = RateLimiter(limit, window)

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await limiter.acquire()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
