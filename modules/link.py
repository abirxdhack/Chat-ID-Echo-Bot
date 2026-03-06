from telethon import events, Button
from telethon.tl.types import User, KeyboardButtonCopy
from utils import LOGGER
from utils.helpers import format_user_response, format_chat_response, get_profile_photo
from bot import bot
from config import COMMAND_PREFIX

_PREFIX = "".join(COMMAND_PREFIX)

def _clean(text):
    return text.strip().lstrip("@").replace("https://","").replace("http://","").replace("t.me/","").replace("/","").replace(":","")

def _user_buttons(entity, full_name):
    return [
        [Button.url("Android Link", f"tg://openmessage?user_id={entity.id}"), Button.url("IOS Link", f"https://t.me/@id{entity.id}")],
        [KeyboardButtonCopy(text=full_name, copy_text=str(entity.id))],
    ]

def _chat_buttons(entity):
    raw_id = str(entity.id).lstrip("-")
    return [[Button.url("Join Link", f"https://t.me/c/{raw_id}/10000000")]]

async def _edit_with_entity(chat_id, msg, entity_id):
    entity = await bot.get_entity(entity_id)
    response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
    buttons = _user_buttons(entity, full_name) if isinstance(entity, User) else _chat_buttons(entity)
    photo = await get_profile_photo(bot, entity_id)
    if photo:
        try:
            await bot.edit_message(chat_id, msg.id, response, file=photo, buttons=buttons, parse_mode="md")
            return
        except Exception as e:
            LOGGER.error(f"Photo failed {entity_id}: {e}")
    await msg.edit(response, buttons=buttons, parse_mode="md", link_preview=False)

@bot.on(events.CallbackQuery(pattern=rb"^get_link_(-?\d+)$"))
async def handle_link_callback(event):
    entity_id = int(event.pattern_match.group(1).decode())
    try:
        entity = await bot.get_entity(entity_id)
        response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
        buttons = _user_buttons(entity, full_name) if isinstance(entity, User) else _chat_buttons(entity)
        photo = await get_profile_photo(bot, entity_id)
        if photo:
            try:
                await event.edit(response, file=photo, buttons=buttons, parse_mode="md")
                return
            except Exception as e:
                LOGGER.error(f"Photo failed {entity_id}: {e}")
        await event.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    except Exception as e:
        LOGGER.error(f"Link callback failed {entity_id}: {e}")
        await event.edit("**Looks Like I Don't Have Control Over The Entity**", parse_mode="md")

@bot.on(events.NewMessage(pattern=rf"^[{_PREFIX}]link(\s|$)", func=lambda e: e.is_private))
async def link_command(event):
    LOGGER.info(f"Link command from {event.sender_id}")
    loading = await bot.send_message(event.chat_id, "`Processing Link...`")
    parts = event.text.split()
    if len(parts) == 1 or parts[1].lower() == "me":
        user = await event.get_sender()
        response, full_name = format_user_response(user)
        buttons = [[Button.inline("Get Chat Link", data=f"get_link_{user.id}")]]
        photo = await get_profile_photo(bot, user.id)
        if photo:
            try:
                await bot.edit_message(event.chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                return
            except Exception as e:
                LOGGER.error(f"Photo failed {user.id}: {e}")
        await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    else:
        try:
            entity = await bot.get_entity(_clean(parts[1]))
            response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
            buttons = [[Button.inline("Get Chat Link", data=f"get_link_{entity.id}")]]
            photo = await get_profile_photo(bot, entity.id)
            if photo:
                try:
                    await bot.edit_message(event.chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                    return
                except Exception as e:
                    LOGGER.error(f"Photo failed {entity.id}: {e}")
            await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
        except Exception as e:
            LOGGER.error(f"Link command failed: {e}")
            await loading.edit("**Looks Like I Don't Have Control Over The Entity**", parse_mode="md")
