class Messages:
    """Container for all bot messages."""

    # Command responses
    START_MESSAGE = (
        "Hello! I'm a Haiku Bot 🌸\n\n"
        "I can detect haikus in your messages using the 5-7-5 syllable pattern!\n\n"
        "*Commands:*\n"
        "• /start - Activate the bot\n"
        "• /stop - Deactivate the bot\n"
        "• /mode - Select detection mode\n\n"
        "*Modes:*\n"
        "🎯 STRICT - Only exact haikus (no extra text)\n"
        "🎲 RANDOM - Find haikus in text, return random one\n\n"
        "*Example haiku:*\n"
        "An old silent pond\n"
        "A frog jumps into the pond\n"
        "Splash! Silence again"
    )

    STOP_MESSAGE = "Bot deactivated. Use /start to reactivate."

    MODE_CHANGED_STRICT = "🔧 Detection mode set to: *STRICT*\n\nI'll only detect haikus if your entire message is exactly a haiku with no extra text."

    MODE_CHANGED_RANDOM = "🔧 Detection mode set to: *RANDOM*\n\nI'll search for haikus in your messages and return one random haiku if multiple are found."

    MODE_PROMPT = "🎛️ *Current mode: {mode}*\n\nChoose a detection mode:\n\n🎯 *STRICT* - Only exact haikus (no extra text)\n🎲 *RANDOM* - Find haikus in text, return random one"

    BOT_NOT_ACTIVE = "Bot is not active in this chat. Use /start to activate."
