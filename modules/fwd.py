from telethon import events, Button
from telethon.tl.types import User, MessageFwdHeader
from utils import LOGGER
from utils.helpers import format_user_response, format_chat_response, get_profile_photo
from bot import bot

@bot.on(events.NewMessage(func=lambda e: e.is_private and e.fwd_from is not None))
async def handle_forwarded_message(event):
    LOGGER.info(f"Forwarded msg from {event.sender_id}")
    loading = await bot.send_message(event.chat_id, "`Processing Forwarded Info...`")
    try:
        fwd: MessageFwdHeader = event.fwd_from
        entity_id = None
        response = None
        full_name = None
        if fwd.from_id is not None:
            try:
                entity = await bot.get_entity(fwd.from_id)
                entity_id = entity.id
                response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
            except Exception as e:
                LOGGER.error(f"Forward from_id resolve failed: {e}")
        if response is None:
            full_name = fwd.from_name or "Unknown"
            response = (
                "**🔍 Showing Forwarded User Info 📋**\n"
                "━━━━━━━━━━━━━━━━\n"
                f"**Name:** {full_name}\n"
                "━━━━━━━━━━━━━━━━\n"
                "**👁 Thank You for Using Our Tool ✅**"
            )
        copy_value = str(entity_id) if entity_id else full_name
        buttons = [[Button.inline(full_name, data=f"copy:{copy_value}")]]
        if entity_id:
            photo = await get_profile_photo(bot, entity_id)
            if photo:
                try:
                    await bot.edit_message(event.chat_id, loading.id, response, file=photo, buttons=buttons, parse_mode="md")
                    return
                except Exception as e:
                    LOGGER.error(f"Photo failed {entity_id}: {e}")
        await loading.edit(response, buttons=buttons, parse_mode="md", link_preview=False)
    except Exception as e:
        LOGGER.error(f"Forward handler failed {event.sender_id}: {e}")
        await loading.edit("**Looks Like I Don't Have Control Over The User**", parse_mode="md")
