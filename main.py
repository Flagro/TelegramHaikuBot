import logging
from decouple import config
from bot.telegram_haiku_bot import TelegramHaikuBot


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    tg_bot = TelegramHaikuBot(
        telegram_token=config("TELEGRAM_BOT_TOKEN"),
        allowed_handles=config("ALLOWED_HANDLES", "").split(",") or None,
        admin_handles=config("ADMIN_HANDLES", "").split(",") or None,
        logger=logging.getLogger("HaikuBot"),
    )
    tg_bot.run()


if __name__ == "__main__":
    main()
