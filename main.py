import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import user_menu, order_form

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    # Register routers here
    dp.include_router(user_menu.router)
    dp.include_router(order_form.router)

    from database import init_db
    await init_db()

    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
