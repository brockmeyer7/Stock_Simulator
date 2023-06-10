import os
import requests
from django.shortcuts import render
import urllib.parse

from functools import wraps


def apology(request, message, code=400):
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
    return render(request, "apology.html", {'top': code, 'bottom': escape(message)})


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        quote_url = f"https://finnhub.io/api/v1/quote?symbol={urllib.parse.quote_plus(symbol)}&token={api_key}"
        info_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={urllib.parse.quote_plus(symbol)}&token={api_key}"
        quote_r = requests.get(quote_url)
        info_r = requests.get(info_url)
        quote_r.raise_for_status()
        info_r.raise_for_status()
    except requests.RequestException as e:
        print(e)
        return None

    # Parse response
    try:
        quote = quote_r.json()
        info = info_r.json()
        return {
            "name": info["name"],
            "price": float(quote["c"]),
            "symbol": info["ticker"]
        }
    except (KeyError, TypeError, ValueError) as e:
        print(e)
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
