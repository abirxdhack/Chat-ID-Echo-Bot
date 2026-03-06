from telethon import events
from utils import LOGGER
from miscs.adbtn import admin_buttons
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]admin", func=lambda e: e.is_private))
async def admin_command(event):
    LOGGER.info("Admin command received")
    await bot.send_message(event.chat_id,
        "**🛡️ Channels and Groups Where You Are Admin**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a channel or group where you have admin privileges.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @itsSmartDev",
        buttons=admin_buttons,
    )
