"""Example of WhiteBIT webhook verification endpoint."""

import logging
import os

from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Get webhook public key from environment variable
WEBHOOK_PUBLIC_KEY = os.environ.get("WEBHOOK_PUBLIC_KEY", "your_webhook_public_key")


async def handle_verification(request: web.Request):
    """Handle WhiteBIT webhook verification request.

    This endpoint should respond with 200 OK and return JSON array which contains your public webhook key.
    """
    try:
        # Return the public key as a JSON array
        return web.json_response([WEBHOOK_PUBLIC_KEY])
    except Exception as e:
        logging.error(f"Error handling verification: {e}")
        return web.Response(status=500, text="Internal server error")


async def handle_root(request: web.Request):
    """Handle root endpoint request."""
    return web.Response(text="WhiteBIT Webhook Server")


# Create the application
app = web.Application()
app.add_routes(
    [
        web.get("/", handle_root),
        web.get("/whiteBIT-verification", handle_verification),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)
