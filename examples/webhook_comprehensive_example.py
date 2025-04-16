"""Comprehensive example of WhiteBIT webhook handling."""

import logging
import os

from aiohttp import web

from aiowhitebit.clients.webhook.webhook_client import get_webhook_data_loader
from aiowhitebit.models.webhook import CodeApplyParams, TransactionParams, WebhookRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Get webhook keys from environment variables
WEBHOOK_PUBLIC_KEY = os.environ.get("WEBHOOK_PUBLIC_KEY", "your_webhook_public_key")
WEBHOOK_KEY = os.environ.get("WEBHOOK_KEY", "your_webhook_key")
WEBHOOK_SECRET_KEY = os.environ.get("WEBHOOK_SECRET_KEY", "your_webhook_secret_key")


# Custom handlers for specific webhook methods
def handle_code_apply(req: WebhookRequest) -> None:
    """Custom handler for code.apply webhook method."""
    params = req.params
    if isinstance(params, CodeApplyParams):
        logging.info(f"Custom handler: Code {params.code} applied with ID {req.id}")
        # Here you can implement your business logic for code application
        # For example, update user's balance, grant special permissions, etc.


def handle_deposit_accepted(req: WebhookRequest) -> None:
    """Custom handler for deposit.accepted webhook method."""
    params = req.params
    if isinstance(params, TransactionParams):
        logging.info(f"Custom handler: Deposit of {params.amount} {params.ticker} accepted to {params.address}")
        # Here you can implement your business logic for deposit acceptance
        # For example, update user's pending deposits, send notification, etc.


def handle_deposit_processed(req: WebhookRequest) -> None:
    """Custom handler for deposit.processed webhook method."""
    params = req.params
    if isinstance(params, TransactionParams):
        logging.info(f"Custom handler: Deposit of {params.amount} {params.ticker} processed to {params.address}")
        # Here you can implement your business logic for deposit processing
        # For example, update user's balance, send notification, etc.


def handle_withdraw_successful(req: WebhookRequest) -> None:
    """Custom handler for withdraw.successful webhook method."""
    params = req.params
    if isinstance(params, TransactionParams):
        logging.info(f"Custom handler: Withdrawal of {params.amount} {params.ticker} successful from {params.address}")
        # Here you can implement your business logic for successful withdrawal
        # For example, update user's balance, send notification, etc.


async def handle_verification(request: web.Request):
    """Handle WhiteBIT webhook verification request."""
    try:
        # Return the public key as a JSON array
        return web.json_response([WEBHOOK_PUBLIC_KEY])
    except Exception as e:
        logging.error(f"Error handling verification: {e}")
        return web.Response(status=500, text="Internal server error")


async def handle_webhook(request: web.Request):
    """Handle webhook requests from WhiteBIT."""
    try:
        json_data = await request.json()
        headers = request.headers

        # Log the incoming request
        logging.info(f"Received webhook request: {json_data}")

        # Get webhook data loader with custom keys
        data_loader = get_webhook_data_loader(WEBHOOK_KEY, WEBHOOK_SECRET_KEY)

        # Register custom handlers
        data_loader.register_handler("code.apply", handle_code_apply)
        data_loader.register_handler("deposit.accepted", handle_deposit_accepted)
        data_loader.register_handler("deposit.processed", handle_deposit_processed)
        data_loader.register_handler("withdraw.successful", handle_withdraw_successful)

        # Validate headers
        if data_loader.validate_headers(headers):
            # Parse request and handle it
            req = WebhookRequest(**json_data)
            data_loader.handle_request(req)
            return web.Response(status=200, text="OK")
        else:
            logging.warning("Invalid webhook request headers")
            return web.Response(status=400, text="Invalid request")
    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
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
        web.post("/webhook", handle_webhook),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=8080)
