__all__ = [
    "WhitebitWebhookDataLoader",
    "get_webhook_data_loader",
]

import base64
import hashlib
import hmac
import json
from typing import Optional

from multidict import CIMultiDictProxy

from aiowhitebit.constants import WEBHOOK_KEY, WEBHOOK_SECRET_KEY
from aiowhitebit.webhook_models import WebhookRequest


class WhitebitWebhookDataLoader:
    def __init__(self) -> None:
        self._webhook_key = WEBHOOK_KEY
        self._webhook_secret_key = WEBHOOK_SECRET_KEY
        self.header_keys = [
            "X-TXC-APIKEY",
            "X-TXC-PAYLOAD",
            "X-TXC-SIGNATURE",
        ]
        self.temp_data: Optional[WebhookRequest] = None

    def validate_headers(self, headers: CIMultiDictProxy) -> bool:
        request_keys = ["id", "params", "method"]
        if not all(name in self.header_keys for name in headers.keys()):
            return False
        if not headers["X-TXC-APIKEY"] == self._webhook_key:
            return False
        payload = base64.b64decode(headers["X-TXC-PAYLOAD"]).decode("ascii")
        json_payload: dict = json.loads(payload)
        if not all(key in request_keys for key in json_payload.keys()):
            return False
        temp_hash = hmac.new(
            self._webhook_secret_key.encode("ascii"),
            headers["X-TXC-PAYLOAD"],
            hashlib.sha512,
        ).hexdigest()
        return hmac.compare_digest(temp_hash, headers["X-TXC-SIGNATURE"])

    def handle_code_apply(self) -> None:
        pass

    def handle_deposit_accepted(self) -> None:
        pass

    def handle_deposit_processed(self) -> None:
        pass

    def handle_deposit_canceled(self) -> None:
        pass

    def handle_general_request(self, req: WebhookRequest) -> None:
        self.temp_data = req
        factory = {
            "code.apply": self.handle_code_apply,
            "deposit.accepted": self.handle_deposit_accepted,
            "deposit.processed": self.handle_deposit_processed,
            "deposit.canceled": self.handle_deposit_canceled,
        }
        factory[req.method]()


def get_webhook_data_loader() -> WhitebitWebhookDataLoader:
    return WhitebitWebhookDataLoader()
