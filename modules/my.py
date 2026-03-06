from telethon import events
from utils import LOGGER
from miscs.mybtn import my_buttons
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]my", func=lambda e: e.is_private))
async def my_command(event):
    LOGGER.info("My command received")
    await bot.send_message(event.chat_id,
        "**📚 Your Channels and Groups**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share your channel or group.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @itsSmartDev",
        buttons=my_buttons,
    )
