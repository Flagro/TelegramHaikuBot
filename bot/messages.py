class Messages:
    """Container for all bot messages."""

    # Command responses
    START_MESSAGE = (
        "Hello! I'm a Haiku Bot 🌸\n\n"
        "Send me a message with three lines in a 5-7-5 syllable pattern, "
        "and I'll detect if it's a haiku!\n\n"
        "Example:\n"
        "An old silent pond\n"
        "A frog jumps into the pond\n"
        "Splash! Silence again"
    )

    STOP_MESSAGE = "Goodbye! Use /start if you want to chat again."

    # Haiku detection
    HAIKU_DETECTED_PREFIX = "✨ Haiku detected! ✨\n\n"

    # Log messages
    LOG_BOT_STARTED = "Bot started"
    LOG_HAIKU_DETECTED = "Haiku detected from user {username}"
