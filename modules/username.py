from telethon import events, Button
from telethon.tl.types import User
from utils import LOGGER
from utils.helpers import format_user_response, format_chat_response, get_profile_photo
from bot import bot

@bot.on(events.NewMessage(pattern=r"^@[a-zA-Z0-9_]{4,32}$", func=lambda e: e.is_private))
async def username_command(event):
    LOGGER.info(f"Username from {event.sender_id}: {event.text}")
    loading = await bot.send_message(event.chat_id, "`Processing Username To Info...`")
    try:
        entity = await bot.get_entity(event.text.strip())
        entity_id = entity.id
        response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
        buttons = [[Button.inline(full_name, data=f"copy:{entity_id}")]]
        photo = await get_profile_photo(bot, entity_id)
        if photo:
            try:
                await bot.edit_message(event.chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                return
            except Exception as e:
                LOGGER.error(f"Photo failed {entity_id}: {e}")
        await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    except Exception as e:
        LOGGER.error(f"Username lookup failed: {e}")
        await loading.edit("**Looks Like I Don't Have Control Over The User**", parse_mode="md")
