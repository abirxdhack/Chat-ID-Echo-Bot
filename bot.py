from telethon import TelegramClient
from utils import LOGGER
from config import API_ID, API_HASH, BOT_TOKEN

LOGGER.info("Creating Bot Client From BOT_TOKEN")

bot = TelegramClient(
    "QuickInfoBot",
    int(API_ID),
    API_HASH,
)

LOGGER.info("Bot Client Created Successfully!")
