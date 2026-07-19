import json, re, os, sys
from urllib.request import Request, urlopen, URLError
from urllib.parse import urlencode

URL = "https://shop.iqoo.com/in/product/2057?skuId=8346"
PRODUCT = "iQOO Neo 10R Refurbished (12GB+256GB MoonKnight Titanium)"

try:
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    html = urlopen(req, timeout=30).read().decode("utf-8")

    availability_match = re.search(r'"availability"\s*:\s*"([^"]+)"', html)
    if availability_match:
        in_stock = "InStock" in availability_match.group(1)
    elif "Out of stock" not in html:
        in_stock = True
    else:
        in_stock = False

    if in_stock:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if bot_token and chat_id:
            msg = (
                f"\U0001f514 {PRODUCT} is BACK IN STOCK!\n"
                f"\U000020b9 20,999\n{URL}"
            )
            data = urlencode({"chat_id": chat_id, "text": msg}).encode()
            urlopen(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                data, timeout=15
            )
            sys.exit(0)
except URLError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
