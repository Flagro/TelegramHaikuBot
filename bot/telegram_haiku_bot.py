import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

from bot.haiku_detector import detect_haiku
from bot.haiku_formatter import format_haiku
from bot.messages import Messages


class TelegramHaikuBot:
    def __init__(
        self,
        telegram_token: str,
        allowed_handles: list[str] | None = None,
        admin_handles: list[str] | None = None,
        logger: logging.Logger | None = None,
    ):
        """
        Initialize the Telegram Haiku Bot.

        Args:
            telegram_token: Telegram bot API token
            allowed_handles: Optional list of allowed usernames (without @)
            admin_handles: Optional list of admin usernames (without @)
            logger: Optional logger instance
        """
        self.telegram_token = telegram_token
        self.allowed_handles = allowed_handles
        self.admin_handles = admin_handles
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def run(self) -> None:
        """Run the bot."""
        application = ApplicationBuilder().token(self.telegram_token).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("stop", self.stop_command))

        # Add message handler for haiku detection
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        self.logger.info("Bot started")
        application.run_polling()

    async def start_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the /start command."""
        # Check if user is an admin
        if self.admin_handles and not self._is_admin(update):
            await update.message.reply_text(
                "Sorry, only administrators can start this bot."
            )
            self.logger.warning(
                f"Unauthorized start attempt by user {update.message.from_user.username}"
            )
            return

        await update.message.reply_text(Messages.START_MESSAGE)

    async def stop_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the /stop command."""
        await update.message.reply_text(Messages.STOP_MESSAGE)

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle incoming messages and detect haikus."""
        if not update.message or not update.message.text:
            return

        # Check if user is allowed to use the bot
        if self.allowed_handles and not self._is_allowed(update):
            self.logger.debug(
                f"Message from unauthorized user {update.message.from_user.username} ignored"
            )
            return

        text = update.message.text
        is_haiku, lines = detect_haiku(text)

        if is_haiku:
            formatted_haiku = format_haiku(lines)
            response = f"{Messages.HAIKU_DETECTED_PREFIX}{formatted_haiku}"

            await update.message.reply_text(
                response,
                parse_mode=ParseMode.MARKDOWN,
            )
            self.logger.info(
                "Haiku detected from user {username}".format(
                    username=update.message.from_user.username
                )
            )

    def _is_admin(self, update: Update) -> bool:
        """Check if the user is an admin."""
        if not update.message or not update.message.from_user:
            return False

        username = update.message.from_user.username
        handle = "@" + username if username else None
        return handle in self.admin_handles if handle else False

    def _is_allowed(self, update: Update) -> bool:
        """Check if the user is allowed to use the bot."""
        if not update.message or not update.message.from_user:
            return False

        username = update.message.from_user.username
        handle = "@" + username if username else None
        return handle in self.allowed_handles if handle else False
