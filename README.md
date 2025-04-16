# aiowhitebit

Async Python client for WhiteBit API

## Features

* [Private http V4 API](https://github.com/whitebit-exchange/api-docs/blob/f7ca495281ade44f9f075a91c2e55d5da32a99fd/Private/http-trade-v4.md)
* [Public WS API](https://github.com/whitebit-exchange/api-docs/blob/master/Public/websocket.md)
* [Public http v1](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v1.md)
* [Public http v2](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v2.md)
* [Public http v4](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v4.md)
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
