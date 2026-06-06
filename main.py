import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config.config import config
from handlers import voice, video, audio, style
from loguru import logger
from handlers.callback_handler import router as callback_router
from handlers.register import router as register_router
from handlers.edit_text import (router as edit_router)
from handlers.connect import router as connect_router
from handlers.connect_sheet_link import router as connect_sheet_link_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("bot.log", rotation="1 day", compression="zip")

async def main():
    # Initialize bot and dispatcher with new DefaultBotProperties
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=config.BOT_TOKEN, default=default)
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(voice.router)
    dp.include_router(video.router)
    dp.include_router(audio.router)
    dp.include_router(style.router)
    dp.include_router(callback_router)
    dp.include_router(register_router)
    dp.include_router(edit_router)
    dp.include_router(connect_router)
    dp.include_router(connect_sheet_link_router)

    # Start polling
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
