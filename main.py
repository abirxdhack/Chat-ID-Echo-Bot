import asyncio
import signal
from bot import bot
from config import BOT_TOKEN
from utils import LOGGER
from telethon import events
import core.start
import modules
import shared.chatinfo


@bot.on(events.CallbackQuery(pattern=rb"^copy:(.+)$"))
async def copy_callback(event):
    await event.answer(f"ID: {event.pattern_match.group(1).decode()}", alert=False)


async def main():
    LOGGER.info("Starting QuickInfoBot (Telethon)...")
    await bot.start(bot_token=BOT_TOKEN)
    me = await bot.get_me()
    LOGGER.info(f"QuickInfoBot Started 💥 @{me.username}")
    await bot.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped by user.")
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
    finally:
        LOGGER.info("Shutdown complete.")