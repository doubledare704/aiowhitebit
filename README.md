# aiowhitebit

Async Python client for WhiteBit API

## Features

* [Private http V4 API](https://github.com/whitebit-exchange/api-docs/blob/f7ca495281ade44f9f075a91c2e55d5da32a99fd/Private/http-trade-v4.md)
* [Public WS API](https://github.com/whitebit-exchange/api-docs/blob/master/Public/websocket.md)
  * Enhanced WebSocket events with `event_time` and `update_id` metadata
  * BookTicker WebSocket stream for real-time best bid/ask prices
  * Market depth subscriptions with enhanced metadata support
* [Public http v1](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v1.md)
* [Public http v2](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v2.md)
* [Public http v4](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v4.md)
  * Funding history endpoint for futures markets
* Webhook support with examples
* Rate limiting
* Type hints
* Pydantic models
* Async/await support

## Installation

```bash
pip install aiowhitebit
```

## Quick Start

```python
import asyncio
from aiowhitebit.clients.public import PublicV4Client

async def main():
    client = PublicV4Client()

    # Get market info
    markets = await client.get_market_info()
    print(f"Number of markets: {len(markets)}")

    # Get market activity
    activity = await client.get_market_activity()
    print(f"BTC_USDT last price: {activity.get('BTC_USDT').last_price}")

asyncio.run(main())
```

### New Features in v0.3.0

#### BookTicker WebSocket Stream

```python
import asyncio
from aiowhitebit.clients.websocket import PublicWebSocketClient, SubscribeRequest

async def bookticker_example():
    client = PublicWebSocketClient()

    # Subscribe to BookTicker stream
    response = await client.bookticker_subscribe("BTC_USDT")
    print(f"Subscribed: {response}")

    # Unsubscribe from BookTicker stream
    response = await client.bookticker_unsubscribe("BTC_USDT")
    print(f"Unsubscribed: {response}")

    await client.close()

asyncio.run(bookticker_example())
```

#### Funding History for Futures Markets

```python
import asyncio
from aiowhitebit.clients.public import PublicV4Client

async def funding_history_example():
    client = PublicV4Client()

    # Get funding rate history for BTC_USDT futures
    history = await client.get_funding_history("BTC_USDT")

    for item in history.result:
        print(f"Time: {item.timestamp}, Rate: {item.funding_rate}")

asyncio.run(funding_history_example())
```

#### Enhanced WebSocket Events with Metadata

All WebSocket events now include optional `event_time` and `update_id` fields for better tracking and synchronization:

```python
# WebSocket responses now include metadata
{
    "method": "depth_update",
    "params": {...},
    "event_time": 1640995200000,  # Event timestamp
    "update_id": 12345           # Unique update identifier
}
```

## Documentation

For detailed documentation and examples, visit our [GitHub repository](https://github.com/doubledare704/aiowhitebit).

## Development

```bash
# Clone the repository
git clone https://github.com/doubledare704/aiowhitebit.git
cd aiowhitebit

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## License

MIT License - see LICENSE file for details
