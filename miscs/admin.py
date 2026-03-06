from telethon import Button
from telethon.tl.types import (
    InputKeyboardButtonRequestPeer,
    RequestPeerTypeChat,
    RequestPeerTypeBroadcast,
    ChatAdminRights,
    ReplyKeyboardMarkup,
    KeyboardButtonRow,
)
from utils import LOGGER

_admin_rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=True,
    manage_call=True,
    manage_topics=True,
    post_stories=True,
    edit_stories=True,
    delete_stories=True,
)

admin_buttons = ReplyKeyboardMarkup(
    rows=[
        KeyboardButtonRow(buttons=[
            InputKeyboardButtonRequestPeer(
                text="📢 Channels",
                button_id=10,
                peer_type=RequestPeerTypeBroadcast(user_admin_rights=_admin_rights),
                max_quantity=1,
                name_requested=True,
                username_requested=True,
                photo_requested=True,
            ),
            InputKeyboardButtonRequestPeer(
                text="👥 Groups",
                button_id=11,
                peer_type=RequestPeerTypeChat(user_admin_rights=_admin_rights),
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
    placeholder="Choose a admin chat type",
)

LOGGER.info("Admin buttons initialized")
