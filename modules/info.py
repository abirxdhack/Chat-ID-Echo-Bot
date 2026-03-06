from telethon import events, Button
from telethon.tl.types import User
from utils import LOGGER
from utils.helpers import format_user_response, format_chat_response, get_profile_photo
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

def _clean(text):
    return text.strip().lstrip("@").replace("https://","").replace("http://","").replace("t.me/","").replace("/","").replace(":","")

async def _send_info(chat_id, loading, entity_id):
    try:
        entity = await bot.get_entity(entity_id)
        response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
        buttons = [[Button.inline(full_name, data=f"copy:{entity_id}")]]
        photo = await get_profile_photo(bot, entity_id)
        if photo:
            try:
                await bot.edit_message(chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                return
            except Exception as e:
                LOGGER.error(f"Photo failed {entity_id}: {e}")
        await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    except Exception as e:
        LOGGER.error(f"Entity fetch failed {entity_id}: {e}")
        await loading.edit("**Looks Like I Don't Have Control Over The User**", parse_mode="md")

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}](info|id)(\s|$)", func=lambda e: e.is_private))
async def info_command(event):
    LOGGER.info(f"Info command from {event.sender_id}")
    loading = await bot.send_message(event.chat_id, "`Processing Info...`")
    parts = event.text.split()
    if len(parts) == 1 or parts[1].lower() == "me":
        user = await event.get_sender()
        await _send_info(event.chat_id, loading, user.id)
    else:
        try:
            entity = await bot.get_entity(_clean(parts[1]))
            await _send_info(event.chat_id, loading, entity.id)
        except Exception as e:
            LOGGER.error(f"get_entity failed: {e}")
            await loading.edit("**Looks Like I Don't Have Control Over The User**", parse_mode="md")
