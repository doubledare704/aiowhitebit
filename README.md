# aiowhitebit

Async client for WhiteBit API

## Features

* [Private http V4 API](https://github.com/whitebit-exchange/api-docs/blob/f7ca495281ade44f9f075a91c2e55d5da32a99fd/Private/http-trade-v4.md)
* [Public WS API, but without unsub](https://github.com/whitebit-exchange/api-docs/blob/master/Public/websocket.md)
* Webhook support with example
* [Public http v1](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v1.md)
* [Public http v2](https://github.com/whitebit-exchange/api-docs/blob/main/docs/Public/http-v2.md)

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/aiowhitebit.git
cd aiowhitebit

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Formatting

This project uses Black for code formatting. To format your code, run:

```bash
black --line-length=120 .
```

### Running Tests

```bash
pytest
```
