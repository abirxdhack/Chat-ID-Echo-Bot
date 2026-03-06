from telethon import events
from utils import LOGGER
from miscs.adbtn import admin_buttons
from miscs.mybtn import my_buttons
from miscs.startbtn import menu_buttons
from bot import bot

@bot.on(events.NewMessage(pattern=r"^👥 Admins Chat$", func=lambda e: e.is_private))
async def admin_button_handler(event):
    LOGGER.info("Admins Chat button clicked")
    await bot.send_message(event.chat_id,
        "**🛡️ Channels and Groups Where You Are Admin**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a channel or group where you have admin privileges.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        buttons=admin_buttons,
    )

@bot.on(events.NewMessage(pattern=r"^👑 Owner Chat$", func=lambda e: e.is_private))
async def owner_button_handler(event):
    LOGGER.info("Owner Chat button clicked")
    await bot.send_message(event.chat_id,
        "**📚 Your Channels and Groups**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share your channel or group.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        buttons=my_buttons,
    )

@bot.on(events.NewMessage(pattern=r"^🔙 Back$", func=lambda e: e.is_private))
async def back_button_handler(event):
    LOGGER.info("Back button clicked")
    await bot.send_message(event.chat_id,
        "**👋 Welcome to Chat ID Finder Bot!** 🆔\n\n"
        "**✅ Fetch Any Chat ID Instantly!**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 **Features:**\n"
        "- Supports users, bots, private/public groups & channels\n"
        "- Fast and reliable\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        buttons=menu_buttons,
    )
