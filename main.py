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

# Mapping of button IDs to types and effect IDs (as integers)
TYPES = {
    1: {'name': 'User', 'effect_id': 5107584321108051014},  # 👍 Thumbs Up
    2: {'name': 'Private Channel', 'effect_id': 5046589136895476101},  # 💩 Poop
    3: {'name': 'Public Channel', 'effect_id': 5104841245755180586},  # 🔥 Fire
    4: {'name': 'Private Group', 'effect_id': 5104858069142078462},  # 👎 Thumbs Down
    5: {'name': 'Public Group', 'effect_id': 5046509860389126442},  # 🎉 Confetti
    6: {'name': 'Bot', 'effect_id': 5046509860389126442},  # 🎉 Confetti
    7: {'name': 'Premium User', 'effect_id': 5046509860389126442}  # 🎉 Confetti
}

# Message effect ID for the /start command (as integer)
START_EFFECT_ID = 5104841245755180586  # 🔥 Fire

# Set up logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

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

        # Send the welcome message with the keyboard and fire effect
        try:
            await client.send_message(
                chat_id,
                welcome_text,
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup,
                message_effect_id=START_EFFECT_ID
            )
            logging.info("Sent welcome message with keyboard and fire effect")
        except Exception as e:
            logging.error(f"Failed to send welcome message: {str(e)}")
            # Retry without effect
            await client.send_message(
                chat_id,
                welcome_text,
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup
            )
            logging.info("Retried welcome message without effect")
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
                effect_id = TYPES.get(6, {}).get('effect_id')  # Use Confetti for forwarded messages
                try:
                    await client.send_message(
                        chat_id,
                        response,
                        parse_mode='html',
                        message_effect_id=effect_id
                    )
                    logging.info(f"Sent forwarded message response with effect: {response}")
                except Exception as e:
                    logging.error(f"Failed to send forwarded message response: {str(e)}")
                    # Retry without effect
                    await client.send_message(
                        chat_id,
                        response,
                        parse_mode='html'
                    )
                    logging.info("Retried forwarded message response without effect")
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

            # Get type and effect ID
            type_info = TYPES.get(button_id, {'name': 'Unknown', 'effect_id': None})
            type_ = type_info['name']
            effect_id = type_info['effect_id']

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

                    # Send the response with effect, retry without if it fails
                    try:
                        await client.send_message(
                            chat_id,
                            response,
                            parse_mode='html',
                            message_effect_id=effect_id
                        )
                        logging.info(f"Sent response: {response}")
                    except Exception as e:
                        logging.error(f"Failed to send peer sharing response: {str(e)}")
                        # Retry without effect
                        await client.send_message(
                            chat_id,
                            response,
                            parse_mode='html'
                        )
                        logging.info(f"Retried peer sharing response without effect: {response}")
            else:
                logging.warning("No peers found in the action")
        else:
            logging.info("Service message is not a peer sharing event")

# Run the bot
print("✅Bot Is Up And Running On Telethon")
client.run_until_disconnected()
