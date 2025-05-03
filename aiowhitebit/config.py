"""Configuration for the WhiteBit API."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class APIEndpoints:
    """API endpoints configuration."""

    # V4 endpoints
    MARKET_INFO: Final = "/api/v4/public/markets"
    MARKET_ACTIVITY: Final = "/api/v4/public/ticker"
    DEPTH: Final = "/api/v4/public/orderbook/depth/{market}"
    ASSET_STATUS: Final = "/api/v4/public/assets"
    TIME_V4: Final = "/api/v4/public/time"
    PING_V4: Final = "/api/v4/public/ping"
    COLLATERAL_MARKETS: Final = "/api/v4/public/collateral/markets"
    FUTURES_MARKETS: Final = "/api/v4/public/futures"
    MINING_POOL: Final = "/api/v4/public/mining-pool"
    MAINTENANCE_STATUS = "/api/v4/public/platform/status"
    ORDERBOOK_V4 = "/api/v4/public/orderbook/{market}"  # Updated format
    DEPTH_V4 = "/api/v4/public/orderbook/depth/{market}"  # Corrected URL
    TRADES_V4 = "/api/v4/public/trades/{market}"
    FEE_V4 = "/api/v4/public/fee"

    # V2 endpoints
    MARKET_INFO_V2: Final = "/api/v2/public/markets"
    TICKER_V2: Final = "/api/v2/public/ticker"
    RECENT_TRADES_V2: Final = "/api/v2/public/trades/{market}"
    FEE_V2: Final = "/api/v2/public/fee"
    ASSET_STATUS_V2: Final = "/api/v2/public/assets"
    DEPTH_V2: Final = "/api/v2/public/depth/{market}"

    # V1 endpoints
    MARKET_INFO_V1: Final = "/api/v1/public/markets"
    TICKER_V1: Final = "/api/v1/public/ticker"
    TICKERS_V1: Final = "/api/v1/public/tickers"
    KLINE_V1: Final = "/api/v1/public/kline"
    SYMBOLS_V1: Final = "/api/v1/public/symbols"
    DEPTH_V1: Final = "/api/v1/public/depth/{market}"
    HISTORY_V1: Final = "/api/v1/public/history"


@dataclass(frozen=True)
class RateLimits:
    """Rate limits configuration for different API versions.

    This class defines the rate limits for different versions of the WhiteBit API.
    The values represent the maximum number of requests allowed within the specified time window.
    """

    PUBLIC_V4: Final = 2000  # requests per 10 seconds
    PUBLIC_V2: Final = 1000  # requests per 10 seconds
    PUBLIC_V1: Final = 1000  # requests per 10 seconds
    PRIVATE_V4: Final = 60  # requests per minute
