"""Base client functionality for the WhiteBit API."""

from asyncio import Semaphore
from typing import Any, Callable, Optional, TypeVar

import aiohttp

from aiowhitebit.constants import BASE_URL
from aiowhitebit.exceptions import WhitebitAPIError

T = TypeVar("T")


class HTTPClient:
    """Base HTTP client for making API requests.

    This class provides the core functionality for making HTTP requests,
    managing the client session, and handling rate limiting.
    """

    def __init__(self):
        """Initialize the HTTP client.

        Sets up an empty session and default rate limiter.
        """
        self._session: Optional[aiohttp.ClientSession] = None
        self._rate_limiter = Semaphore(100)  # Default rate limit

    @property
    async def session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp client session.

        Returns:
            An active aiohttp ClientSession instance.
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        """Close the aiohttp client session if it exists and is open."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get(self, url: str) -> Any:
        """Make a GET request to the specified URL.

        Args:
            url: The URL to make the request to.

        Returns:
            The JSON response from the request.

        Raises:
            WhitebitAPIError: If the response status is not 200.
        """
        async with self._rate_limiter:
            session = await self.session
            async with session.get(url) as response:
                if response.status != 200:
                    await self._handle_error_response(response)
                return await response.json(content_type=None)

    async def _handle_error_response(self, response: aiohttp.ClientResponse) -> None:
        try:
            error_data = await response.json()
        except Exception:
            error_data = await response.text()
        raise WhitebitAPIError(response.status, str(error_data))


class BaseClient(HTTPClient):
    """Base client for WhiteBit API endpoints.

    This class extends the HTTPClient with WhiteBit-specific functionality
    for constructing API URLs and making requests to the API endpoints.
    """

    def __init__(self, base_url: str = BASE_URL):
        """Initialize the base client.

        Args:
            base_url: Base URL for the WhiteBit API. Defaults to the official WhiteBit API URL.
        """
        super().__init__()
        self.base_url = base_url

    def request_url(self, path: str) -> str:
        """Construct the full URL for an API endpoint.

        Args:
            path: API endpoint path.

        Returns:
            Full URL for the API endpoint.
        """
        return f"{self.base_url}{path}"

    async def _make_request(self, path: str, converter: Optional[Callable[[dict], T]] = None) -> T:
        full_url = self.request_url(path)
        json_obj = await self.get(full_url)
        return converter(json_obj) if converter else json_obj
