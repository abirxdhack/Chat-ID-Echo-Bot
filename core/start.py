from telethon import events
from utils import LOGGER
from miscs.startbtn import menu_buttons
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]start", func=lambda e: e.is_private))
async def start(event):
    LOGGER.info("Start command received")
    await bot.send_message(event.chat_id,
        "**👋 Welcome to Quick Info Bot!** 🆔\n\n"
        "**✅ Fetch Any Chat ID Instantly!**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 **Features:**\n"
        "- Supports users, bots, private/public groups & channels\n"
        "- Fast and reliable\n\n"
        "> 🛠 Made with ❤️ By @itsSmartDev",
        buttons=menu_buttons,
    )
