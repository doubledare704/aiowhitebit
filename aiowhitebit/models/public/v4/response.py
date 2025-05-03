"""Response models for the WhiteBit Public API v4."""

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from aiowhitebit.models.base import BaseResponse


class MaintenanceStatus(BaseModel):
    """Maintenance status model for v4 API.

    Attributes:
        status: 1 - system operational, 0 - system maintenance
    """

    status: Union[str, int]

    model_config = ConfigDict(frozen=True, extra="ignore")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Convert any status to string for consistency."""
        return str(v)


class Market(BaseModel):
    """Market information model for v4 API.

    Attributes:
        name: Market pair name
        stock: Ticker of stock currency
        money: Ticker of money currency
        stockPrec: Stock currency precision
        moneyPrec: Precision of money currency
        feePrec: Fee precision
        makerFee: Default maker fee ratio
        takerFee: Default taker fee ratio
        minAmount: Minimal amount of stock to trade
        minTotal: Minimal amount of money to trade
        maxTotal: Maximum total(amount * price) of money to trade
        tradesEnabled: Is trading enabled
        isCollateral: Is margin trading enabled
        type: Market type. Possible values: "spot", "futures"
    """

    name: str
    stock: str
    money: str
    stockPrec: str
    moneyPrec: str
    feePrec: str
    makerFee: str
    takerFee: str
    minAmount: str
    minTotal: str
    maxTotal: str
    tradesEnabled: bool
    isCollateral: bool = False
    type: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class MarketInfo(list[dict[str, Any]]):
    """Market information response model for v4 API.

    This is a list of dictionaries with market information
    """

    pass


class MarketActivityItem(BaseModel):
    """Market activity item model for v4 API.

    Attributes:
        base_id: CoinmarketCap Id of base currency; 0 - if unknown
        quote_id: CoinmarketCap Id of quote currency; 0 - if unknown
        last_price: Last price
        quote_volume: Volume in quote currency
        base_volume: Volume in base currency
        isFrozen: Identifies if trades are closed
        change: Change in percent between open and last prices
    """

    base_id: int
    quote_id: int
    last_price: str
    quote_volume: str
    base_volume: str
    isFrozen: bool
    change: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class MarketActivity(dict[str, MarketActivityItem]):
    """Market activity response model for v4 API.

    This is a dictionary where keys are market names and values are MarketActivityItem objects
    """

    pass


class MinLimit(BaseModel):
    """Minimum limit model."""

    min: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class NetworkTypeLimit(BaseModel):
    """Network type specific limits (e.g., ERC20)."""

    ERC20: MinLimit

    model_config = ConfigDict(frozen=True, extra="ignore")


class Limits(BaseModel):
    """Limits model for v4 API."""

    deposit: NetworkTypeLimit
    withdraw: NetworkTypeLimit

    model_config = ConfigDict(frozen=True, extra="ignore")


class Networks(BaseModel):
    """Networks model for v4 API."""

    default: Optional[str] = None  # e.g. "ERC20"
    deposits: Optional[list[str]] = []  # e.g. ["ERC20"]
    withdraws: Optional[list[str]] = []  # e.g. ["ERC20"]

    model_config = ConfigDict(frozen=True, extra="ignore")


class Asset(BaseModel):
    """Asset model for v4 API."""

    name: str  # e.g. "1inch"
    unified_cryptoasset_id: int  # e.g. 8104
    can_withdraw: bool  # e.g. True
    can_deposit: bool  # e.g. True
    min_withdraw: str  # e.g. "1.5"
    max_withdraw: str  # e.g. "0"
    maker_fee: str  # e.g. "0.1"
    taker_fee: str  # e.g. "0.1"
    min_deposit: str  # e.g. "15"
    max_deposit: str  # e.g. "0"
    currency_precision: int  # e.g. 18
    is_memo: bool  # e.g. False
    networks: Networks
    limits: dict[str, dict[str, dict[str, str]]]  # Nested dict for limits structure
    confirmations: Optional[dict[str, int]] = {}  # e.g. {"ERC20": 32}
    providers: Optional[dict[str, list[str]]] = None

    model_config = ConfigDict(frozen=True, extra="ignore")


class AssetStatus(dict[str, Asset]):
    """Asset status response model for v4 API."""

    pass


class OrderbookItem(BaseModel):
    """Orderbook item model for v4 API.

    Attributes:
        price: Price level
        amount: Amount at this price level
    """

    price: str
    amount: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class Orderbook(BaseModel):
    """Orderbook model for v4 API.

    Attributes:
        ticker_id: Market Name
        timestamp: Current timestamp
        asks: Array of ask orders
        bids: Array of bid orders
    """

    ticker_id: str
    timestamp: int
    asks: list[list[str]]
    bids: list[list[str]]

    model_config = ConfigDict(frozen=True, extra="ignore")


class Depth(Orderbook):
    """Depth model for v4 API.

    This is the same as Orderbook but retrieves depth price levels within ±2% of the market last price
    """

    pass


class RecentTrade(BaseModel):
    """Recent trade model for v4 API.

    Attributes:
        tradeID: A unique ID associated with the trade for the currency pair transaction
        price: Transaction price in quote pair volume
        quote_volume: Transaction amount in quote pair volume
        base_volume: Transaction amount in base pair volume
        trade_timestamp: Unix timestamp in milliseconds, identifies when the transaction occurred
        type: Used to determine whether or not the transaction originated as a buy or sell
    """

    tradeID: int
    price: str
    quote_volume: str
    base_volume: str
    trade_timestamp: int
    type: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class RecentTrades(list[RecentTrade]):
    """Recent trades response model for v4 API.

    This is a list of RecentTrade objects
    """

    pass


class FeeFlex(BaseModel):
    """Fee flex model for v4 API.

    Attributes:
        min_fee: Min fee amount
        max_fee: Max fee amount
        percent: Fee percentage
    """

    min_fee: str
    max_fee: str
    percent: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class FeeDetails(BaseModel):
    """Fee details model for v4 API.

    Attributes:
        min_amount: Min deposit/withdraw amount. 0 if there is no limitation
        max_amount: Max deposit/withdraw amount. 0 if there is no limitation
        fixed: Fixed fee amount which applies for all transaction
        flex: Flex fee only applies for all transactions but according to min/max fee
        is_depositable: True if currency can be depositable (optional)
        is_withdrawal: True if currency can be withdrawable (optional)
        is_api_withdrawal: True if currency can be withdrawable by api (optional)
        is_api_depositable: True if currency can be depositable by api (optional)
        name: Provider name (optional)
        ticker: Provider ticker (optional)
    """

    min_amount: str
    max_amount: str
    fixed: Optional[str] = None
    flex: Optional[FeeFlex] = None
    is_depositable: Optional[bool] = None
    is_withdrawal: Optional[bool] = None
    is_api_withdrawal: Optional[bool] = None
    is_api_depositable: Optional[bool] = None
    name: Optional[str] = None
    ticker: Optional[str] = None

    model_config = ConfigDict(frozen=True, extra="ignore")


class Fee(BaseModel):
    """Fee model for v4 API.

    Attributes:
        ticker: Currency ticker
        name: Currency name
        providers: List of providers
        deposit: Deposit fees
        withdraw: Withdraw fees
        is_depositable: True if currency can be depositable
        is_withdrawal: True if currency can be withdrawable
        is_api_withdrawal: True if currency can be withdrawable by api
        is_api_depositable: True if currency can be depositable by api
    """

    ticker: str
    name: str
    providers: list[str] = []
    deposit: Union[FeeDetails, dict[str, FeeDetails]]
    withdraw: Union[FeeDetails, dict[str, FeeDetails]]
    is_depositable: bool
    is_withdrawal: bool
    is_api_withdrawal: bool
    is_api_depositable: bool

    model_config = ConfigDict(frozen=True, extra="ignore")


class FeeResponse(dict[str, Fee]):
    """Fee response model for v4 API.

    This is a dictionary where keys are currency names and values are Fee objects
    """

    pass


class ServerTime(BaseModel):
    """Server time model for v4 API.

    Attributes:
        time: Current server time
    """

    time: int

    model_config = ConfigDict(frozen=True, extra="ignore")


class ServerStatus(list[str]):
    """Server status response model for v4 API.

    This is a list with a single string "pong"
    """

    pass


class CollateralMarkets(list[str]):
    """Collateral markets response model for v4 API.

    This is a list of market names that are available for collateral trading
    """

    pass


class FuturesBrackets(BaseModel):
    """Futures brackets model for v4 API.

    Attributes:
        1: Bracket value for leverage 1
        2: Bracket value for leverage 2
        3: Bracket value for leverage 3
        5: Bracket value for leverage 5
        10: Bracket value for leverage 10
        20: Bracket value for leverage 20
        50: Bracket value for leverage 50
        100: Bracket value for leverage 100
    """

    bracket_1: int = Field(0, alias="1")
    bracket_2: int = Field(0, alias="2")
    bracket_3: int = Field(0, alias="3")
    bracket_5: int = Field(0, alias="5")
    bracket_10: int = Field(0, alias="10")
    bracket_20: int = Field(0, alias="20")
    bracket_50: int = Field(0, alias="50")
    bracket_100: int = Field(0, alias="100")

    model_config = ConfigDict(frozen=True, extra="ignore", populate_by_name=True)


class FuturesMarket(BaseModel):
    """Futures market model for v4 API.

    Attributes:
        ticker_id: Identifier of a ticker with delimiter to separate base/target
        stock_currency: Symbol/currency code of base pair
        money_currency: Symbol/currency code of target pair
        last_price: Last transacted price of base currency based on given target currency
        stock_volume: 24 hour trading volume in base pair volume
        money_volume: 24 hour trading volume in target pair volume
        bid: Current highest bid price
        ask: Current lowest ask price
        high: Rolling 24-hours highest transaction price
        low: Rolling 24-hours lowest transaction price
        product_type: What product is this? Futures, Perpetual, Options?
        open_interest: The open interest in the last 24 hours in contracts
        index_price: Underlying index price
        index_name: Name of the underlying index if any
        index_currency: Underlying currency for index
        funding_rate: The current funding rate, which may fluctuate due to market conditions
        next_funding_rate_timestamp: Timestamp of the next funding rate change
        brackets: Brackets
        max_leverage: Max Leverage
    """

    ticker_id: str
    stock_currency: str
    money_currency: str
    last_price: str
    stock_volume: str
    money_volume: str
    bid: str
    ask: str
    high: str
    low: str
    product_type: str
    open_interest: str
    index_price: str
    index_name: str
    index_currency: str
    funding_rate: str
    next_funding_rate_timestamp: str
    brackets: FuturesBrackets
    max_leverage: int

    model_config = ConfigDict(frozen=True, extra="ignore")


class FuturesMarketsResult(BaseModel):
    """Futures markets result model for v4 API.

    Attributes:
        result: List of futures markets
    """

    result: list[FuturesMarket]

    model_config = ConfigDict(frozen=True, extra="ignore")


class FuturesMarkets(BaseResponse):
    """Futures markets response model for v4 API.

    Attributes:
        success: Whether the request was successful
        message: Error message if success is False, None otherwise
        result: List of futures markets
    """

    result: list[FuturesMarket]

    model_config = ConfigDict(frozen=True, extra="ignore")


class MiningPoolHashRate(BaseModel):
    """Mining pool hash rate model."""

    timestamp: int
    hashrate: str

    model_config = ConfigDict(frozen=True, extra="ignore")


class MiningPoolBlock(BaseModel):
    """Mining pool block model."""

    blockFoundAt: int
    blockHeight: int

    model_config = ConfigDict(frozen=True, extra="ignore")


class MiningPoolData(BaseModel):
    """Mining pool data model."""

    assets: list[str]
    blocks: list[MiningPoolBlock]
    connectionLinks: list[str]
    currentHashRate: str
    last7daysHashRate: list[MiningPoolHashRate]
    location: str
    rewardSchemes: list[str]
    workers: int

    model_config = ConfigDict(frozen=True, extra="ignore")


class MiningPoolOverview(BaseModel):
    """Mining pool overview response model."""

    data: MiningPoolData

    model_config = ConfigDict(frozen=True, extra="ignore")
