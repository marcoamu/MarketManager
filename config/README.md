# Configuration Guide

## Environment Variables

This application uses environment variables for sensitive configuration. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

## Required Variables

### Alpaca Trading API
- `ALPACA_API_KEY` - Your Alpaca API key
- `ALPACA_API_SECRET` - Your Alpaca API secret
- `ALPACA_BASE_URL` - API endpoint (default: https://paper-api.alpaca.markets)
- `ALPACA_PAPER_MODE` - Use paper trading (default: true)

### Telegram Service
- `TELEGRAM_APP_ID` - Telegram application ID
- `TELEGRAM_APP_API_HASH` - Telegram API hash
- `TELEGRAM_TOKEN_BOT` - Bot token for notifications
- `TELEGRAM_PHONE_NUMBER` - Your phone number for authentication
- `TELEGRAM_CHAT_ID` - Default chat ID for messages
- `TELEGRAM_GROUP_ID` - Default group ID for messages

## Security

**IMPORTANT**: Never commit the `.env` file to version control. It's already in `.gitignore`.

## Legacy Config

The `config.ini` file is being phased out in favor of environment variables and YAML-based configuration per asset (see `config/actives/`).
