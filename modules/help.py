from telethon import events, Button
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX, ADMIN_ID

_PREFIX = "".join(COMMAND_PREFIX)

_HELP = "**Here Are QuickInfo Bot Options 👇:**\n\n"
_FORWARD = (
    "**Forward Message Tutorial 📬**\n\n"
    "🔎 Want to grab the ID of a user or chat? Just forward a message to me! Here's how:\n\n"
    "1️⃣ Find a message in any chat (user, group, channel, or bot).\n"
    "2️⃣ Forward it to me privately.\n"
    "3️⃣ I'll instantly reveal the ID, name, and more! ⚡\n\n"
    "💡 **Pro Tip:** Works with any forwarded message, even from private chats! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_GETME = (
    "**Get Me Tutorial 🙋‍♂️**\n\n"
    "🔍 Want to know your own Telegram ID? It's super easy!\n\n"
    "1️⃣ Just type `/me` in the chat with me.\n"
    "2️⃣ I'll send your user ID, name, and username instantly! ⚡\n"
    "3️⃣ If you have a profile photo, I'll show it too! 📸\n\n"
    "💡 **Pro Tip:** Use the button in the reply to copy your ID! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_SHAREDCHAT = (
    "**Shared Chat Tutorial 🌐**\n\n"
    "🔎 Need the ID of a user, group, or channel? Share it with me!\n\n"
    "1️⃣ Type `/start` to see the sharing buttons.\n"
    "2️⃣ Pick a user, bot, group, or channel to share.\n"
    "3️⃣ I'll fetch the ID, name, and username instantly! ⚡\n\n"
    "💡 **Pro Tip:** Works for public and private chats, plus bots and premium users! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_ADMINS = (
    "**Admins Tutorial 🛡️**\n\n"
    "🔍 Want to see where you're an admin? I've got you!\n\n"
    "1️⃣ Type `/admin` in the chat with me.\n"
    "2️⃣ Use the buttons to share a channel or group where you have admin rights.\n"
    "3️⃣ I'll reveal the ID and details instantly! ⚡\n\n"
    "💡 **Pro Tip:** Perfect for managing your admin roles! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_OWNCHATS = (
    "**Own Chats Tutorial 📚**\n\n"
    "🔎 Curious about your own channels or groups? Let's find them!\n\n"
    "1️⃣ Type `/my` in the chat with me.\n"
    "2️⃣ Use the buttons to share a channel or group you own.\n"
    "3️⃣ I'll send the ID and details in a snap! ⚡\n\n"
    "💡 **Pro Tip:** Great for keeping track of your own chats! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_USERNAME = (
    "**Username Tutorial 👤**\n\n"
    "🔎 Want info about a specific user? Just send me their username!\n\n"
    "1️⃣ Type a username (e.g., `@username`) in the chat with me.\n"
    "2️⃣ I'll fetch their ID, name, and other details instantly! ⚡\n"
    "3️⃣ If they have a profile photo, I'll show it too! 📸\n\n"
    "💡 **Pro Tip:** Works for any public username, even bots! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_LINK = (
    "**Link Tutorial 🔗**\n\n"
    "🔎 Want to get a direct link to a user, bot, group, or channel? It's simple!\n\n"
    "1️⃣ Type `/link` or `/link @username` in the chat with me.\n"
    "2️⃣ I'll show the profile info and a button to get the link! ⚡\n"
    "3️⃣ Click 'Get Chat Link' to reveal Android, iOS, or join links! 😎\n\n"
    "💡 **Pro Tip:** Works for any user, bot, or chat, even private ones! 🚀\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)
_INLINE_TPL = (
    "**Inline Mode Tutorial 🔍**\n\n"
    "🔎 Want to fetch info about a user or chat using inline mode? It's super simple!\n\n"
    "1️⃣ Type my username in any chat, followed by one of these:\n"
    "   - Username: `{b} @username`\n"
    "   - User ID: `{b} userid`\n"
    "   - Chat ID: `{b} chatid`\n"
    "   - Link: `{b} t.me/username`\n"
    "   - URL: `{b} https://t.me/username`\n"
    "2️⃣ Select the result to get the ID, name, and more! ⚡\n"
    "3️⃣ Supports 5 types of input for maximum flexibility! 😎\n\n"
    "💡 **Pro Tip:** Use inline mode in any chat, even groups or channels! 🚀\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

_TEXTS = {
    "help_forward": _FORWARD, "help_getme": _GETME, "help_sharedchat": _SHAREDCHAT,
    "help_admins": _ADMINS, "help_ownchats": _OWNCHATS, "help_username": _USERNAME,
    "help_link": _LINK,
}

_MAIN_BTNS = [
    [Button.inline("📬 Forward", b"help_forward"), Button.inline("🙋‍♂️ Get Me", b"help_getme")],
    [Button.inline("🌐 Shared Chat", b"help_sharedchat"), Button.inline("🛡️ Admins", b"help_admins")],
    [Button.inline("📚 Own Chats", b"help_ownchats"), Button.inline("🔍 Inline", b"help_inline")],
    [Button.inline("👤 Username", b"help_username"), Button.inline("🤖 Link", b"help_link")],
    [Button.inline("Close ❌", b"help_close"), Button.url("🔧 Dev", f"tg://user?id={ADMIN_ID}")],
    [Button.url("🔔 Join For Updates", "https://t.me/itsSmartDev")],
]
_BACK_BTN = [[Button.inline("Back", b"main_menu")]]

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]help", func=lambda e: e.is_private))
async def help_command(event):
    LOGGER.info(f"Help command from {event.sender_id}")
    await bot.send_message(event.chat_id, _HELP, buttons=_MAIN_BTNS, parse_mode="md", link_preview=False)

@bot.on(events.CallbackQuery(pattern=rb"^(help_forward|help_getme|help_sharedchat|help_admins|help_ownchats|help_username|help_link|help_inline|help_close|main_menu)$"))
async def handle_help_callback(event):
    data = event.data.decode()
    LOGGER.info(f"Help callback {data} from {event.sender_id}")
    if data == "help_close":
        try:
            await event.delete()
        except Exception as e:
            LOGGER.error(f"Delete failed: {e}")
            await event.edit(_HELP, buttons=_MAIN_BTNS, parse_mode="md", link_preview=False)
    elif data == "main_menu":
        await event.edit(_HELP, buttons=_MAIN_BTNS, parse_mode="md", link_preview=False)
    elif data == "help_inline":
        me = await bot.get_me()
        await event.edit(_INLINE_TPL.format(b=f"@{me.username}"), buttons=_BACK_BTN, parse_mode="md", link_preview=False)
    else:
        await event.edit(_TEXTS[data], buttons=_BACK_BTN, parse_mode="md", link_preview=False)
