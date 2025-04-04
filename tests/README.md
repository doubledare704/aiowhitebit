# Tests for aiowhitebit

This directory contains tests for the aiowhitebit library.

## Running Tests

To run the tests, use pytest:

```bash
pytest
```

Or to run a specific test file:

```bash
pytest tests/public/test_public_v1_client.py
```

## Code Formatting

This project uses Black for code formatting. To format your code, run:

```bash
black --line-length=120 .
```

You can also install pre-commit hooks to automatically format your code before committing:

```bash
pip install pre-commit
pre-commit install
```

## Test Structure

- `tests/public/`: Tests for public API clients
  - `test_public_v1_client.py`: Tests for the Public API v1 client
  - `test_converters.py`: Tests for the converter functions

## Adding New Tests

When adding new tests, follow these guidelines:

1. Create a new test file in the appropriate directory
2. Use pytest fixtures for setup and teardown
3. Use pytest.mark.asyncio for testing async functions
4. Mock external API calls using unittest.mock
5. Test both success and error cases
6. Test parameter validation
