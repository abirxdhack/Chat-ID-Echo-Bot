from telethon import Button
from telethon.tl.types import (
    InputKeyboardButtonRequestPeer,
    RequestPeerTypeChat,
    RequestPeerTypeBroadcast,
    ReplyKeyboardMarkup,
    KeyboardButtonRow,
)
from utils import LOGGER

my_buttons = ReplyKeyboardMarkup(
    rows=[
        KeyboardButtonRow(buttons=[
            InputKeyboardButtonRequestPeer(
                text="📢 Your Channel",
                button_id=9,
                peer_type=RequestPeerTypeBroadcast(creator=True),
                max_quantity=1,
                name_requested=True,
                username_requested=True,
                photo_requested=True,
            ),
            InputKeyboardButtonRequestPeer(
                text="👥 Your Group",
                button_id=8,
                peer_type=RequestPeerTypeChat(creator=True),
                max_quantity=1,
                name_requested=True,
                username_requested=True,
                photo_requested=True,
            ),
        ]),
        KeyboardButtonRow(buttons=[
            Button.text("🔙 Back").button,
        ]),
    ],
    resize=True,
    placeholder="Choose a own chat type",
)

LOGGER.info("My buttons initialized")
