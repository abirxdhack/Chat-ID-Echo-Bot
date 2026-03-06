from telethon import events, Button
from telethon.tl.types import User, UpdateBotInlineSend
from utils import LOGGER
from utils.helpers import format_user_response, format_chat_response, get_profile_photo
from bot import bot

_cache: dict = {}

def _clean(text):
    return text.strip().lstrip("@").replace("https://","").replace("http://","").replace("t.me/","").replace("/","").replace(":","")

def _search_btns():
    return [Button.switch_inline("🔍 Search", query="", same_peer=True), Button.switch_inline("🔍 Search in Chat", query="")]

@bot.on(events.InlineQuery())
async def inline_query_handler(event):
    LOGGER.info(f"InlineQuery from {event.sender_id}: {event.text!r}")
    builder = event.builder
    me = await bot.get_me()
    bot_uname = f"@{me.username}"

    if not event.text.strip():
        await event.answer([
            await builder.article(
                "Enter a username",
                text=f"**Please enter a username after {bot_uname} (e.g., {bot_uname} @username)**",
                description="Type a username to get info",
                id="placeholder",
                parse_mode="md",
                link_preview=False,
                buttons=[[Button.switch_inline("🔍 Search", query="", same_peer=True)], [Button.switch_inline("🔍 Search in Chat", query="")]],
            )
        ], cache_time=1)
        return

    identifier = _clean(event.text)
    result_id = identifier.replace("-", "m")
    try:
        entity = await bot.get_entity(identifier)
        eid = entity.id
        response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
        _cache[result_id] = {"entity_id": eid, "response": response, "full_name": full_name}
        await event.answer([
            await builder.article(
                title=full_name,
                description=f"ID: {eid}",
                text=f"**⏳ Fetching Info…**\n\n**{full_name}**",
                id=result_id,
                parse_mode="md",
                link_preview=False,
                buttons=[
                    [Button.inline(full_name, data=f"copy:{eid}")],
                    [Button.switch_inline("🔍 Search", query="", same_peer=True), Button.switch_inline("🔍 Search in Chat", query="")],
                ],
            )
        ], cache_time=1)
        LOGGER.info(f"Inline answered for {identifier}")
    except Exception as e:
        LOGGER.error(f"Inline query error for {identifier}: {e}")
        await event.answer([
            await builder.article(
                "Error",
                text="**Looks Like I Don't Have Control Over The User**",
                description="Could not fetch info",
                id="error",
                parse_mode="md",
                link_preview=False,
                buttons=[[Button.switch_inline("🔍 Search", query="", same_peer=True)], [Button.switch_inline("🔍 Search in Chat", query="")]],
            )
        ], cache_time=1)

@bot.on(events.Raw(UpdateBotInlineSend))
async def chosen_inline_result(update: UpdateBotInlineSend):
    result_id = update.id
    msg_id = update.msg_id
    LOGGER.info(f"UpdateBotInlineSend | user={update.user_id} | id={result_id!r} | msg_id={msg_id}")
    if msg_id is None or result_id in ("placeholder", "error"):
        return
    cached = _cache.get(result_id)
    if cached:
        entity_id, response, full_name = cached["entity_id"], cached["response"], cached["full_name"]
        LOGGER.info(f"Cache HIT | {result_id!r}")
    else:
        LOGGER.warning(f"Cache MISS | {result_id!r}")
        try:
            entity = await bot.get_entity(result_id.replace("m", "-"))
            entity_id = entity.id
            response, full_name = format_user_response(entity) if isinstance(entity, User) else format_chat_response(entity)
        except Exception as e:
            LOGGER.error(f"Re-fetch failed {result_id}: {e}")
            try:
                await bot.edit_message(msg_id, "**Looks Like I Don't Have Control Over The User**", parse_mode="md")
            except Exception:
                pass
            return
    buttons = [
        [Button.inline(full_name, data=f"copy:{entity_id}")],
        [Button.switch_inline("🔍 Search", query="", same_peer=True), Button.switch_inline("🔍 Search in Chat", query="")],
    ]
    photo = await get_profile_photo(bot, entity_id)
    if photo:
        try:
            await bot.edit_message(msg_id, response, file=photo, buttons=buttons, parse_mode="md")
            LOGGER.info(f"Inline edit with photo OK | {entity_id}")
            return
        except Exception as e:
            LOGGER.warning(f"Inline photo edit failed {entity_id}: {e}")
    try:
        await bot.edit_message(msg_id, response, buttons=buttons, parse_mode="md", link_preview=False)
        LOGGER.info(f"Inline edit text OK | {entity_id}")
    except Exception as e:
        LOGGER.error(f"Inline edit failed {entity_id}: {e}")
