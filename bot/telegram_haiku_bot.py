import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode

from bot.haiku_detector import detect_haiku, detect_haiku_strict, detect_all_haikus
from bot.haiku_formatter import format_haiku
from bot.messages import Messages
from bot.chat_state import ChatStateManager, DetectionMode


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
        self.state_manager = ChatStateManager()

    def run(self) -> None:
        """Run the bot."""
        application = ApplicationBuilder().token(self.telegram_token).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("stop", self.stop_command))
        application.add_handler(CommandHandler("mode", self.mode_command))

        # Add callback query handler for inline keyboard buttons
        application.add_handler(CallbackQueryHandler(self.button_callback))

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
        if not update.message or not update.effective_chat:
            return

        # Check if user is an admin (if admin list is configured, empty/None = allow all)
        if (
            self.admin_handles
            and len(self.admin_handles) > 0
            and not self._is_admin(update)
        ):
            await update.message.reply_text(
                "Sorry, only administrators can start this bot."
            )
            self.logger.warning(
                f"Unauthorized start attempt by user {update.message.from_user.username}"
            )
            return

        # Activate bot for this chat
        chat_id = update.effective_chat.id
        self.state_manager.set_active(chat_id, True)

        await update.message.reply_text(
            Messages.START_MESSAGE,
            parse_mode=ParseMode.MARKDOWN,
        )
        self.logger.info(f"Bot activated in chat {chat_id}")

    async def stop_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the /stop command."""
        if not update.message or not update.effective_chat:
            return

        # Deactivate bot for this chat
        chat_id = update.effective_chat.id
        self.state_manager.set_active(chat_id, False)

        await update.message.reply_text(Messages.STOP_MESSAGE)
        self.logger.info(f"Bot deactivated in chat {chat_id}")

    async def mode_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the /mode command - shows keyboard to select detection mode."""
        if not update.message or not update.effective_chat:
            return

        chat_id = update.effective_chat.id
        current_mode = self.state_manager.get_mode(chat_id)
        mode_name = current_mode.value.upper()

        # Create inline keyboard with mode options
        keyboard = [
            [
                InlineKeyboardButton("🎯 STRICT", callback_data="mode_strict"),
                InlineKeyboardButton("🎲 RANDOM", callback_data="mode_random"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            Messages.MODE_PROMPT.format(mode=mode_name),
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    async def button_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle button presses from inline keyboards."""
        query = update.callback_query
        if not query or not query.message or not update.effective_chat:
            return

        await query.answer()

        chat_id = update.effective_chat.id

        # Handle mode selection
        if query.data == "mode_strict":
            self.state_manager.set_mode(chat_id, DetectionMode.STRICT)
            await query.edit_message_text(
                Messages.MODE_CHANGED_STRICT,
                parse_mode=ParseMode.MARKDOWN,
            )
            self.logger.info(f"Detection mode set to STRICT in chat {chat_id}")
        elif query.data == "mode_random":
            self.state_manager.set_mode(chat_id, DetectionMode.RANDOM)
            await query.edit_message_text(
                Messages.MODE_CHANGED_RANDOM,
                parse_mode=ParseMode.MARKDOWN,
            )
            self.logger.info(f"Detection mode set to RANDOM in chat {chat_id}")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle incoming messages and detect haikus."""
        if not update.message or not update.message.text or not update.effective_chat:
            return

        chat_id = update.effective_chat.id

        # Check if bot is active in this chat
        if not self.state_manager.is_active(chat_id):
            self.logger.debug(f"Bot is not active in chat {chat_id}, ignoring message")
            return

        # Check if user is allowed to use the bot (if allowed list is configured, empty/None = allow all)
        if (
            self.allowed_handles
            and len(self.allowed_handles) > 0
            and not self._is_allowed(update)
        ):
            self.logger.debug(
                f"Message from unauthorized user {update.message.from_user.username} ignored"
            )
            return

        text = update.message.text
        detection_mode = self.state_manager.get_mode(chat_id)

        if detection_mode == DetectionMode.STRICT:
            # STRICT mode: Only detect if entire message is exactly a haiku
            is_haiku, lines = detect_haiku_strict(text)

            if is_haiku:
                formatted_haiku = format_haiku(lines)
                response = f"{Messages.HAIKU_DETECTED_PREFIX}{formatted_haiku}"

                await update.message.reply_text(
                    response,
                    parse_mode=ParseMode.MARKDOWN,
                )
                self.logger.info(
                    f"Haiku detected (strict mode) from user {update.message.from_user.username} in chat {chat_id}"
                )
        else:
            # RANDOM mode: Find all haikus and return one random one
            haikus = detect_all_haikus(text)

            if haikus:
                # Pick one random haiku from all found
                selected_haiku = random.choice(haikus)
                formatted_haiku = format_haiku(selected_haiku)
                response = f"{Messages.HAIKU_DETECTED_PREFIX}{formatted_haiku}"

                await update.message.reply_text(
                    response,
                    parse_mode=ParseMode.MARKDOWN,
                )
                self.logger.info(
                    f"Haiku detected (random mode, {len(haikus)} found) from user {update.message.from_user.username} in chat {chat_id}"
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
