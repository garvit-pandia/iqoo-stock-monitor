import re, os, sys, datetime
from urllib.request import Request, urlopen, URLError
from urllib.parse import urlencode

URL = "https://shop.iqoo.com/in/product/2057"

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

def send_alert(text):
    if bot_token and chat_id:
        data = urlencode({"chat_id": chat_id, "text": text}).encode()
        urlopen(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data, timeout=15
        )

# Daily heartbeat at 9:00 AM IST (3:30 UTC)
now = datetime.datetime.now(datetime.UTC)
if now.hour == 3 and 25 <= now.minute <= 35:
    send_alert("✅ Heartbeat — iQOO stock monitor is still running.")
    print("Heartbeat sent")

try:
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    html = urlopen(req, timeout=30).read().decode("utf-8")

    # Check JSON-LD first (most reliable overall indicator)
    jsonld_match = re.search(r'"availability"\s*:\s*"([^"]+)"', html)
    overall_in_stock = jsonld_match and "InStock" in jsonld_match.group(1)

    # Check all variants by searching for skuName + marketable in context
    target_names = [
        "8GB+256GB Raging Blue",
        "8GB+256GB MoonKnight Titanium",
        "12GB+256GB Raging Blue",
        "12GB+256GB MoonKnight Titanium",
    ]

    in_stock = []
    for name in target_names:
        escaped = re.escape(name)
        pattern = rf'skuName:"[^"]*{escaped}[^"]*"[^;]{{0,500}}?marketable:(\w+)'
        m = re.search(pattern, html)
        if m:
            if m.group(1) in ('t', 'true', '1'):
                in_stock.append(name)
        else:
            # If pattern not found, the variant may be in a variable assignment.
            # Try broader search by color + GB
            parts = name.split()
            if 'MoonKnight' in name:
                color_part = 'MoonKnight'
            else:
                color_part = 'Raging Blue'
            gb_part = name.split()[0]
            broad_pattern = rf'{gb_part}[^.]{{0,500}}{re.escape(color_part)}[^.]{{0,500}}marketable:(\w+)'
            m2 = re.search(broad_pattern, html)
            if m2 and m2.group(1) in ('t', 'true', '1'):
                in_stock.append(name)

    if in_stock:
        msg = "\U0001f514 iQOO Neo 10R Refurbished BACK IN STOCK!\n\n"
        for v in in_stock:
            sku_id = {"8GB+256GB Raging Blue": "8343",
                       "8GB+256GB MoonKnight Titanium": "8344",
                       "12GB+256GB Raging Blue": "8345",
                       "12GB+256GB MoonKnight Titanium": "8346"}.get(v, "")
            link = f"https://shop.iqoo.com/in/product/2057?skuId={sku_id}" if sku_id else URL
            msg += f"  \u2705 {v}\n    {link}\n"
        send_alert(msg)
        print("ALERT: Variants in stock:", in_stock)
    elif overall_in_stock:
        send_alert("\U0001f514 iQOO Neo 10R Refurbished may be in stock! Check: " + URL)
        print("ALERT: Overall page shows in stock but couldn't identify variants")
    else:
        print("All variants still out of stock")

except URLError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
