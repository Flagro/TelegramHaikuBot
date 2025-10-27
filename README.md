# TelegramHaikuBot

A simple Telegram bot that detects haikus in messages. When a message with a 5-7-5 syllable pattern is detected, the bot will reply with the haiku formatted in italic.

## Features

- Detects haikus (three lines with 5-7-5 syllable pattern)
- Formats detected haikus in italic
- Simple `/start` and `/stop` commands

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Create a `.env` file with your bot token:
```
TELEGRAM_BOT_TOKEN=your_token_here
ALLOWED_HANDLES=  # Optional: comma-separated list of allowed usernames
ADMIN_HANDLES=    # Optional: comma-separated list of admin usernames
```

3. Run the bot:
```bash
poetry run python main.py
```

## Example

Send a message like:

```
An old silent pond
A frog jumps into the pond
Splash! Silence again
```

The bot will detect it and reply with the haiku formatted in italic.
