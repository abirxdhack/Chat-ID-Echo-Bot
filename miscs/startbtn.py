from telethon import Button
from telethon.tl.types import (
    InputKeyboardButtonRequestPeer,
    RequestPeerTypeUser,
    RequestPeerTypeChat,
    RequestPeerTypeBroadcast,
    ReplyKeyboardMarkup,
    KeyboardButtonRow,
)
from utils import LOGGER


def _peer_btn(text, button_id, peer_type, max_quantity=1,
              name_requested=True, username_requested=True, photo_requested=True):
    return InputKeyboardButtonRequestPeer(
        text=text,
        button_id=button_id,
        peer_type=peer_type,
        max_quantity=max_quantity,
        name_requested=name_requested,
        username_requested=username_requested,
        photo_requested=photo_requested,
    )


menu_buttons = ReplyKeyboardMarkup(
    rows=[
        KeyboardButtonRow(buttons=[
            _peer_btn("👤 User Info",       1, RequestPeerTypeUser(bot=False)),
        ]),
        KeyboardButtonRow(buttons=[
            _peer_btn("👥 Public Group",    7, RequestPeerTypeChat(has_username=True)),
            _peer_btn("🔒 Private Group",   6, RequestPeerTypeChat(has_username=False)),
        ]),
        KeyboardButtonRow(buttons=[
            _peer_btn("📢 Public Channel",  5, RequestPeerTypeBroadcast(has_username=True)),
            _peer_btn("🔒 Private Channel", 4, RequestPeerTypeBroadcast(has_username=False)),
        ]),
        KeyboardButtonRow(buttons=[
            _peer_btn("🤖 Bot",             2, RequestPeerTypeUser(bot=True)),
            _peer_btn("🌟 Premium Users",   3, RequestPeerTypeUser(bot=False, premium=True)),
        ]),
        KeyboardButtonRow(buttons=[
            Button.text("👥 Admins Chat").button,
            Button.text("👑 Owner Chat").button,
        ]),
    ],
    resize=True,
    placeholder="Choose a chat type",
)

LOGGER.info("Menu buttons initialized")
