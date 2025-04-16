import logging
from telethon import TelegramClient, events, utils
from telethon.tl.types import (
    KeyboardButtonRequestPeer, ReplyKeyboardMarkup, KeyboardButtonRow,
    RequestPeerTypeUser, RequestPeerTypeChat, RequestPeerTypeBroadcast,
    UpdateNewMessage, MessageService,
    RequestedPeerUser, RequestedPeerChat, RequestedPeerChannel,
    PeerUser, PeerChat, PeerChannel, User, Chat, Channel
)
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Start the Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Handle new messages for /start command and forwarded messages
@client.on(events.NewMessage)
async def handle_new_message(event):
    message = event.message
    chat_id = event.chat_id
    text = message.text

    # Log every incoming message
    logging.info(f"Received NewMessage: text='{text}', chat_id={chat_id}, message={message}")

    if text == '/start':
        logging.info("Processing /start command")
        welcome_text = (
            "👋 <b>Welcome to Chat ID Finder Bot!</b> 🆔\n\n"
            "✅ <b>Fetch Any Chat ID Instantly!</b>\n\n"
            "🔧 <b>How to Use?</b>\n"
            "1️⃣ Click the buttons below to share a chat or user.\n"
            "2️⃣ Receive the unique ID instantly.\n\n"
            "💎 <b>Features:</b>\n"
            "✅ Supports users, bots, groups & channels\n"
            "⚡ Fast and reliable\n\n"
            "<blockquote>🛠 Made with ❤️ by @TheSmartDev</blockquote>"
        )

        # Define the keyboard buttons
        keyboard = [
            [KeyboardButtonRequestPeer(
                text='👤 User',
                button_id=1,
                peer_type=RequestPeerTypeUser(bot=False),
                max_quantity=1
            )],
            [KeyboardButtonRequestPeer(
                text='🔒 Private Channel',
                button_id=2,
                peer_type=RequestPeerTypeBroadcast(has_username=False),
                max_quantity=1
            ), KeyboardButtonRequestPeer(
                text='🌐 Public Channel',
                button_id=3,
                peer_type=RequestPeerTypeBroadcast(has_username=True),
                max_quantity=1
            )],
            [KeyboardButtonRequestPeer(
                text='🔒 Private Group',
                button_id=4,
                peer_type=RequestPeerTypeChat(has_username=False),
                max_quantity=1
            ), KeyboardButtonRequestPeer(
                text='🌐 Public Group',
                button_id=5,
                peer_type=RequestPeerTypeChat(has_username=True),
                max_quantity=1
            )],
            [KeyboardButtonRequestPeer(
                text='🤖 Bot',
                button_id=6,
                peer_type=RequestPeerTypeUser(bot=True),
                max_quantity=1
            ), KeyboardButtonRequestPeer(
                text='Premium 🌟',
                button_id=7,
                peer_type=RequestPeerTypeUser(premium=True),
                max_quantity=1
            )]
        ]

        # Create the reply markup
        reply_markup = ReplyKeyboardMarkup(
            rows=[KeyboardButtonRow(buttons=row) for row in keyboard],
            resize=True,
            single_use=False
        )

        # Send the welcome message with the keyboard
        await client.send_message(
            chat_id,
            welcome_text,
            parse_mode='html',
            link_preview=False,
            buttons=reply_markup
        )
        logging.info("Sent welcome message with keyboard")
    elif message.forward is not None:
        # Handle forwarded message
        peer = message.forward.saved_from_peer or message.forward.from_id
        if peer:
            chat_id_forwarded = utils.get_peer_id(peer)
            try:
                entity = await client.get_entity(peer)
                if isinstance(entity, User):
                    chat_name = entity.first_name or "User"
                elif isinstance(entity, (Chat, Channel)):
                    chat_name = entity.title
                else:
                    chat_name = "Unknown"
                response = (
                    f"<b>Forward Message Detected</b>\n"
                    f"<b>Chat Name {chat_name}</b>\n"
                    f"<b>ChatID {chat_id_forwarded}</b>"
                )
            except ValueError:
                response = "<b>Sorry Bro, Forward Method Not Support For Private Things</b>"
            
            await client.send_message(chat_id, response, parse_mode='html')
            logging.info(f"Sent response: {response}")
        else:
            logging.info("Forwarded message but no peer found")

# Handle raw updates to capture peer sharing
@client.on(events.Raw)
async def handle_raw_update(update):
    logging.info(f"Received raw update: {update}")

    # Check if this update is a new message with a service action
    if isinstance(update, UpdateNewMessage) and isinstance(update.message, MessageService):
        message = update.message
        chat_id = message.peer_id.user_id if hasattr(message.peer_id, 'user_id') else message.peer_id.chat_id
        logging.info(f"Service message detected: {message}")

        # Check if the service message is related to peer sharing
        if hasattr(message.action, 'button_id') and hasattr(message.action, 'peers'):
            logging.info("Detected peer sharing action")
            button_id = message.action.button_id
            peers = message.action.peers

            # Map button IDs to types
            types = {
                1: 'User',
                2: 'Private Channel',
                3: 'Public Channel',
                4: 'Private Group',
                5: 'Public Group',
                6: 'Bot',
                7: 'Premium User'
            }
            type_ = types.get(button_id, 'Unknown')

            # Process each shared peer
            if peers:
                for peer in peers:
                    logging.info(f"Processing shared peer: {peer}")
                    if isinstance(peer, RequestedPeerUser):
                        user_id = peer.user_id
                        response = f"👤 <b>Shared {type_} Info</b>\n🆔 ID: <code>{user_id}</code>"
                    elif isinstance(peer, RequestedPeerChat):
                        chat_id_shared = -peer.chat_id  # Group chat IDs are negative
                        response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{chat_id_shared}</code>"
                    elif isinstance(peer, RequestedPeerChannel):
                        channel_id = -1000000000000 - peer.channel_id  # Channel IDs start with -100...
                        response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{channel_id}</code>"
                    else:
                        response = "Looks Like I Don't Have Control Over The User"
                        logging.warning("Unknown peer type encountered")

                    # Send the response
                    await client.send_message(chat_id, response, parse_mode='html')
                    logging.info(f"Sent response: {response}")
            else:
                logging.warning("No peers found in the action")
        else:
            logging.info("Service message is not a peer sharing event")

# Run the bot
print("✅Bot Is Up And Running On Telethon")
client.run_until_disconnected()
