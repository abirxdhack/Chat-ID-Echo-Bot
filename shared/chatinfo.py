from telethon import events
from telethon.tl.types import (
    UpdateNewMessage,
    MessageService,
    MessageActionRequestedPeerSentMe,
    RequestedPeerUser,
    RequestedPeerChat,
    RequestedPeerChannel,
    KeyboardButtonCopy,
    Photo,
)
from utils import LOGGER
from bot import bot


@bot.on(events.Raw(UpdateNewMessage))
async def handle_message(update: UpdateNewMessage):
    msg = update.message
    if not isinstance(msg, MessageService):
        return
    if not isinstance(msg.action, MessageActionRequestedPeerSentMe):
        return

    LOGGER.info("Shared peer received")

    for peer in msg.action.peers:
        try:
            if isinstance(peer, RequestedPeerUser):
                first_name = getattr(peer, 'first_name', '') or ''
                last_name  = getattr(peer, 'last_name',  '') or ''
                full_name  = f"{first_name} {last_name}".strip() or "Unknown"
                username   = f"@{peer.username}" if getattr(peer, 'username', None) else "No username"
                display_id = peer.user_id
                text = (
                    f"**Shared User Info**\n"
                    f"Type: `User`\n"
                    f"ID: `{display_id}`\n"
                    f"Name: `{full_name}`\n"
                    f"Username: `{username}`"
                )

            elif isinstance(peer, RequestedPeerChat):
                full_name  = getattr(peer, 'title', None) or "Unnamed Chat"
                display_id = -peer.chat_id if peer.chat_id > 0 else peer.chat_id
                text = (
                    f"**Shared Group Info**\n"
                    f"Type: `Group`\n"
                    f"ID: `{display_id}`\n"
                    f"Name: `{full_name}`\n"
                    f"Username: `No username`"
                )

            elif isinstance(peer, RequestedPeerChannel):
                full_name  = getattr(peer, 'title', None) or "Unnamed Channel"
                username   = f"@{peer.username}" if getattr(peer, 'username', None) else "No username"
                display_id = int(f"-100{peer.channel_id}")
                text = (
                    f"**Shared Channel Info**\n"
                    f"Type: `Channel`\n"
                    f"ID: `{display_id}`\n"
                    f"Name: `{full_name}`\n"
                    f"Username: `{username}`"
                )

            else:
                LOGGER.warning(f"Unknown peer type: {type(peer)}")
                continue

            buttons = [[KeyboardButtonCopy(text=full_name, copy_text=str(display_id))]]
            photo = getattr(peer, 'photo', None)
            photo = photo if isinstance(photo, Photo) else None

            if photo:
                try:
                    await bot.send_message(msg.peer_id, text, file=photo, buttons=buttons, parse_mode="md")
                    continue
                except Exception as e:
                    LOGGER.error(f"Photo send failed: {e}")

            await bot.send_message(msg.peer_id, text, buttons=buttons, parse_mode="md")

        except Exception as e:
            LOGGER.error(f"Shared peer handler error {peer}: {e}")