import logging

from aiohttp import web

from aiowhitebit.clients.webhook.webhook_client import get_webhook_data_loader
from aiowhitebit.models.webhook import WebhookRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# Custom handlers for specific webhook methods
def handle_deposit_processed(req: WebhookRequest) -> None:
    """Custom handler for deposit.processed webhook method."""
    logging.info(f"Custom handler: Deposit processed with ID {req.id}")


async def handle_webhook(request: web.Request):
    """Handle webhook requests from WhiteBIT."""
    try:
        json_data = await request.json()
        headers = request.headers

        # Get webhook data loader
        data_loader = get_webhook_data_loader()

        # Register custom handlers
        data_loader.register_handler("deposit.processed", handle_deposit_processed)

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


app = web.Application()
app.add_routes(
    [web.post("/webhook", handle_webhook)],
)

if __name__ == "__main__":
    web.run_app(app, port=8081)
