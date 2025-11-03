# TelegramHaikuBot

A Telegram bot that detects haikus in messages using intelligent pattern recognition. The bot can find haikus anywhere within longer text messages and supports multiple detection modes.

## Features

- **Smart Detection**: Finds haikus embedded in any continuous text, not just perfectly formatted messages
- **Flexible Modes**: Choose between detecting the first haiku or all haikus in a message
- **Per-Chat Settings**: Each chat/group has independent state and configuration
- **Dynamic Configuration**: Change detection mode on-the-fly with commands
- **Beautiful Formatting**: Detected haikus are formatted in italic for emphasis
- **Access Control**: Optional whitelist for allowed users and administrators

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

## Commands

- `/start` - Activate the bot in the current chat
- `/stop` - Deactivate the bot in the current chat
- `/mode` - Open keyboard to select detection mode (STRICT or RANDOM)

## Detection Modes

### 🎯 STRICT Mode (Default)
Only detects haikus if your **entire message** is exactly a haiku with no extra text. Perfect for when you want to share a pure haiku.

**Example:**
```
An old silent pond
A frog jumps into the pond
Splash! Silence again
```
✓ Bot will respond - this is exactly a haiku!

```
Hey! An old silent pond A frog jumps into the pond Splash! Silence again
```
✗ Bot won't respond - extra text before the haiku

### 🎲 RANDOM Mode
Searches your entire message for haikus and returns one randomly selected haiku if multiple are found. Great for conversations where haikus might appear naturally!

**Example:**
```
Here are my haikus: An old silent pond A frog jumps into the pond splash silence again. And another: Over the wintry forest winds howl in a rage with no leaves to blow.
```
✓ Bot will find both haikus and return one randomly!

## Usage Examples

### 1. Activate and Set Mode

```
User: /start
Bot: Hello! I'm a Haiku Bot 🌸 [...]

User: /mode
Bot: 🎛️ Current mode: STRICT
     [Shows keyboard with STRICT and RANDOM buttons]

User: [Clicks RANDOM button]
Bot: 🔧 Detection mode set to: RANDOM
```

### 2. STRICT Mode Example

```
User: An old silent pond
      A frog jumps into the pond
      Splash! Silence again

Bot: 🌸 Haiku detected:
     _An old silent pond_
     _A frog jumps into the pond_
     _Splash! Silence again_
```

### 3. RANDOM Mode Example

```
User: I wrote some haikus today. An old silent pond A frog jumps into 
      the pond splash silence again. Here's another one Over the wintry 
      forest winds howl in a rage with no leaves to blow. What do you think?

Bot: 🌸 Haiku detected:
     _Over the wintry_
     _forest winds howl in a rage_
     _with no leaves to blow_
```
(Randomly selected from the multiple haikus found)

## How It Works

### Detection Algorithm

The bot uses a sliding window algorithm to scan through messages:

1. **STRICT Mode**: Checks if the entire message (all words) forms exactly one 5-7-5 haiku
2. **RANDOM Mode**: Scans through the message to find all possible 5-7-5 patterns, then randomly selects one

### Chat State Management

Each chat/group maintains independent state:
- **Active/Inactive**: Whether the bot responds to messages (use `/start` and `/stop`)
- **Detection Mode**: STRICT (exact match) or RANDOM (search and pick random)

States are stored in-memory during the bot's runtime.
