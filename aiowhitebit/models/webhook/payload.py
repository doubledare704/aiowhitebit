"""Webhook payload models."""

__all__ = [
    "WebhookRequest",
    "WebhookParams",
    "CodeApplyParams",
    "TransactionParams",
    "ConfirmationsInfo",
]

from typing import Dict, Any, Optional, Union

from pydantic import BaseModel, validator


class WebhookParams(BaseModel):
    """Base webhook params model.

    Attributes:
        nonce: A number that is always greater than the previous request's nonce number
    """

    nonce: Optional[int] = None


class CodeApplyParams(WebhookParams):
    """Code apply webhook params model.

    Attributes:
        code: WhiteBIT code that was applied
    """

    code: str


class ConfirmationsInfo(BaseModel):
    """Confirmations info model.

    Attributes:
        actual: Current block confirmations
        required: Required block confirmation for successful deposit
    """

    actual: int
    required: int


class TransactionParams(WebhookParams):
    """Base transaction webhook params model.

    Attributes:
        address: Wallet address
        amount: Amount of transaction
        createdAt: Timestamp of transaction
        currency: Transaction currency
        description: Transaction description
        fee: Transaction fee
        memo: Transaction memo
        method: Called method (1 - deposit, 2 - withdraw)
        network: Currency network (if currency is multi network)
        status: Transaction status
        ticker: Currency ticker
        transactionHash: Transaction hash
        uniqueId: Unique ID of transaction
        confirmations: Confirmations info (if transaction has confirmations)
    """

    address: str
    amount: str
    createdAt: int
    currency: str
    description: Optional[str] = None
    fee: str
    memo: str = ""
    method: Optional[int] = None
    network: Optional[str] = None
    status: Optional[int] = None
    ticker: str
    transactionHash: str
    uniqueId: Optional[str] = None
    confirmations: Optional[ConfirmationsInfo] = None

    @validator("method")
    def validate_method(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError("Method must be 1 (deposit) or 2 (withdraw)")
        return v


class WebhookRequest(BaseModel):
    """Webhook request model.

    Attributes:
        method: The name of method which was evaluated
        params: The request payload
        id: UUID to identify every request
    """

    method: str
    params: Union[WebhookParams, CodeApplyParams, TransactionParams, Dict[str, Any]]
    id: str

    @validator("params", pre=True)
    def validate_params(cls, v, values):
        method = values.get("method", "")

        if method == "code.apply":
            return CodeApplyParams(**v)
        elif method in [
            "deposit.accepted",
            "deposit.updated",
            "deposit.processed",
            "deposit.canceled",
            "withdraw.unconfirmed",
            "withdraw.pending",
            "withdraw.canceled",
            "withdraw.successful",
        ]:
            return TransactionParams(**v)

        return v
