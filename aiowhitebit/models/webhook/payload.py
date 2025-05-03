"""Webhook payload models."""

__all__ = [
    "CodeApplyParams",
    "ConfirmationsInfo",
    "TransactionParams",
    "WebhookParams",
    "WebhookRequest",
]

from typing import Any, Optional, Union

from pydantic import BaseModel, field_validator


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

    @field_validator("method")
    @classmethod
    def validate_method(cls, v):
        """Validate that method is one of the allowed values.

        Args:
            v: The method value to validate.

        Returns:
            The validated method value.

        Raises:
            ValueError: If the method is not one of the allowed values.
        """
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
    params: Union[WebhookParams, CodeApplyParams, TransactionParams, dict[str, Any]]
    id: str

    @field_validator("params", mode="before")
    @classmethod
    def validate_params(cls, v, info):
        """Validate and convert params based on the method.

        Args:
            v: The params value to validate.
            info: Validation context information.

        Returns:
            The validated and converted params value.
        """
        method = info.data.get("method", "")

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
