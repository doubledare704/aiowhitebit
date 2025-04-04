from aiohttp import web

from aiowhitebit.clients.webhook.webhook_client import get_webhook_data_loader
from aiowhitebit.models.webhook import WebhookRequest


async def handle_webhook(request: web.Request):
    json = await request.json()
    headers = request.headers
    data_loader = get_webhook_data_loader()
    if data_loader.validate_headers(headers):
        data_loader.handle_general_request(WebhookRequest(**json))
        return web.Response()
    return web.Response(status=400)


app = web.Application()
app.add_routes(
    [web.post("/webhook", handle_webhook)],
)

if __name__ == "__main__":
    web.run_app(app, port=8081)
