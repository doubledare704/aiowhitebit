from typing import Dict

import aiohttp


async def base_get_request(url) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json()
