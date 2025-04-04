"""Base client functionality for the WhiteBit API."""

from typing import Any

import aiohttp


async def base_get_request(url: str) -> Any:
    """Base GET request handler

    Args:
        url: Full URL for the API endpoint

    Returns:
        JSON response from the API
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            # Allow both application/json and text/plain content types
            return await r.json(content_type=None)
