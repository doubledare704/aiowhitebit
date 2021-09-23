import os

BASE_URL = "https://whitebit.com"
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

KNOWN_ERRORS = {
    1: "- market is disabled for trading",
    2: "- incorrect amount (it is less than or equals zero or its precision is too big)",
    3: "- incorrect price (it is less than or equals zero or its precision is too big)",
    4: "- incorrect taker fee (it is less than zero or its precision is too big)",
    5: "- incorrect maker fee (it is less than zero or its precision is too big)",
    6: "- incorrect clientOrderId (invalid string or not unique id)",
}
