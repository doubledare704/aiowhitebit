"""Base client functionality for the WhiteBit API."""
from asyncio import Semaphore
from typing import Any, Optional, TypeVar, Callable

import aiohttp

from aiowhitebit.constants import BASE_URL
from aiowhitebit.exceptions import WhitebitAPIError

T = TypeVar('T')


class HTTPClient:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._rate_limiter = Semaphore(100)  # Default rate limit

    @property
    async def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get(self, url: str) -> Any:
        async with self._rate_limiter:
            session = await self.session
            async with session.get(url) as response:
                if response.status != 200:
                    await self._handle_error_response(response)
                return await response.json(content_type=None)

    async def _handle_error_response(self, response: aiohttp.ClientResponse) -> None:
        try:
            error_data = await response.json()
        except:
            error_data = await response.text()
        raise WhitebitAPIError(response.status, str(error_data))


class BaseClient(HTTPClient):
    def __init__(self, base_url: str = BASE_URL):
        super().__init__()
        self.base_url = base_url

    def request_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def _make_request(
            self,
            path: str,
            converter: Optional[Callable[[dict], T]] = None
    ) -> T:
        full_url = self.request_url(path)
        json_obj = await self.get(full_url)
        return converter(json_obj) if converter else json_obj


