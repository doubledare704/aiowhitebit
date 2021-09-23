import logging

from aiowhitebit.constants import KNOWN_ERRORS


class WhitebitException(Exception):
    pass


def handle_errors(resp: dict) -> None:
    if "code" in resp and resp["code"] in KNOWN_ERRORS:
        logging.error(f"KNOWN_ERROR: {KNOWN_ERRORS[resp['code']]}")
    logging.error(f"Error occured during request: {resp}")
    raise WhitebitException()
