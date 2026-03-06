from telethon import events, Button
from utils import LOGGER
from utils.helpers import format_user_response, get_profile_photo
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]me(\s|$)", func=lambda e: e.is_private))
async def me_command(event):
    LOGGER.info(f"Me command from {event.sender_id}")
    loading = await bot.send_message(event.chat_id, "`Processing Your Info...`")
    try:
        user = await event.get_sender()
        response, full_name = format_user_response(user)
        buttons = [[Button.inline(full_name, data=f"copy:{user.id}")]]
        photo = await get_profile_photo(bot, user.id)
        if photo:
            try:
                await bot.edit_message(event.chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                return
            except Exception as e:
                LOGGER.error(f"Photo failed {user.id}: {e}")
        await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    except Exception as e:
        LOGGER.error(f"Me command failed {event.sender_id}: {e}")
        await loading.edit("**Looks Like I Don't Have Control Over The User**", parse_mode="md")
