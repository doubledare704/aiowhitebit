"""Models for the WhiteBit API."""

from aiowhitebit.models.base import (
    BaseResponse,
    BasePublicV1Response,
    BasePublicV2Response,
    BasePrivateResponse,
    BaseWebSocketResponse,
)
from aiowhitebit.models.public.v1 import *
from aiowhitebit.models.public.v2 import *
from aiowhitebit.models.private import *
from aiowhitebit.models.websocket import *
