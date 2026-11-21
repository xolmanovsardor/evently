import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("telegram_bot")


async def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN sozlanmagan! Iltimos, .env faylini tekshiring.")
        return

    logger.info("Evently Telegram Bot ishga tushirilmoqda...")
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    try:
        # Polling rejimida botni yurgizish
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot polling boshlandi...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
