import os
# import requests
from django.shortcuts import render
import urllib.parse

from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render("apology.html", {'top': code, 'bottom': escape(message)}), code


# def lookup(symbol):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         api_key = os.environ.get("API_KEY")
#         url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

#     # Parse response
#     try:
#         quote = response.json()
#         return {
#             "name": quote["companyName"],
#             "price": float(quote["latestPrice"]),
#             "symbol": quote["symbol"]
#         }
#     except (KeyError, TypeError, ValueError):
        # return None


# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"
