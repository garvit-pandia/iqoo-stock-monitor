# iQOO Neo 10R Refurbished Stock Monitor

Checks every 30 minutes via GitHub Actions (free, runs in cloud, no laptop needed).

## Setup

1. **Create a Telegram bot** — message [@BotFather](https://t.me/BotFather) on Telegram:
   - `/newbot` → name it → get a token like `123:ABC`

2. **Get your Chat ID** — message [@userinfobot](https://t.me/userinfobot) → get your ID

3. **Fork this repo** or create a new one on GitHub

4. **Add secrets** → GitHub repo → Settings → Secrets and variables → Actions:
   - `TELEGRAM_BOT_TOKEN` — the token from BotFather
   - `TELEGRAM_CHAT_ID` — your user ID

5. **Enable Actions** → GitHub repo → Actions → enable workflows

That's it. When stock comes back, Telegram will ping you immediately.
