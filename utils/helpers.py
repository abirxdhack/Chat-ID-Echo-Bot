from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from telethon.tl.types import (
    User, Channel, Chat,
    UserStatusOnline, UserStatusOffline, UserStatusRecently,
    UserStatusLastWeek, UserStatusLastMonth, UserStatusEmpty,
)
from utils import LOGGER


def calculate_account_age(creation_date):
    today = datetime.now()
    delta = relativedelta(today, creation_date)
    return f"{delta.years} years, {delta.months} months, {delta.days} days"


def estimate_account_creation_date(user_id):
    reference_points = [
        (100000000,  datetime(2013, 8, 1)),
        (1273841502, datetime(2020, 8, 13)),
        (1500000000, datetime(2021, 5, 1)),
        (2000000000, datetime(2022, 12, 1)),
    ]
    closest_point = min(reference_points, key=lambda x: abs(x[0] - user_id))
    closest_user_id, closest_date = closest_point
    id_difference = user_id - closest_user_id
    days_difference = id_difference / 20000000
    return closest_date + timedelta(days=days_difference)


def get_status_display(status):
    if status is None:
        return "Unknown"
    if isinstance(status, UserStatusOnline):
        return "Online"
    if isinstance(status, UserStatusOffline):
        return "Offline"
    if isinstance(status, UserStatusRecently):
        return "Recently"
    if isinstance(status, UserStatusLastWeek):
        return "Last Week"
    if isinstance(status, UserStatusLastMonth):
        return "Last Month"
    if isinstance(status, UserStatusEmpty):
        return "Long Ago"
    return "Unknown"


def get_dc_location(dc_id):
    dc_locations = {
        1:  "MIA, Miami, USA, US",
        2:  "AMS, Amsterdam, Netherlands, NL",
        3:  "MBA, Mumbai, India, IN",
        4:  "STO, Stockholm, Sweden, SE",
        5:  "SIN, Singapore, SG",
        6:  "LHR, London, United Kingdom, GB",
        7:  "FRA, Frankfurt, Germany, DE",
        8:  "JFK, New York, USA, US",
        9:  "HKG, Hong Kong, HK",
        10: "TYO, Tokyo, Japan, JP",
        11: "SYD, Sydney, Australia, AU",
        12: "GRU, São Paulo, Brazil, BR",
        13: "DXB, Dubai, UAE, AE",
        14: "CDG, Paris, France, FR",
        15: "ICN, Seoul, South Korea, KR",
    }
    return dc_locations.get(dc_id, "Unknown")


async def get_profile_photo(client, entity_id):
    try:
        photos = await client.get_profile_photos(entity_id, limit=1)
        if photos:
            return photos[0]
    except Exception as e:
        LOGGER.error(f"Error getting profile photo for {entity_id}: {e}")
    return None


def format_user_response(user, is_group_context=False, chat=None):
    is_bot = getattr(user, 'bot', False)
    is_premium = getattr(user, 'premium', False)
    dc_id = getattr(user.photo, 'dc_id', 0) if user.photo else 0
    dc_location = get_dc_location(dc_id)
    account_created = estimate_account_creation_date(user.id)
    account_created_str = account_created.strftime("%B %d, %Y")
    account_age = calculate_account_age(account_created)
    first_name = getattr(user, 'first_name', None) or 'Unknown'
    last_name = getattr(user, 'last_name', None)
    full_name = first_name if not last_name else f"{first_name} {last_name}".strip()
    profile_type = "Bot's Profile Info" if is_bot else "User's Profile Info"

    response = (
        f"**🔍 Showing {profile_type} 📋**\n"
        "━━━━━━━━━━━━━━━━\n"
        f"**Full Name:** {full_name}\n"
    )
    username = getattr(user, 'username', None)
    if username:
        response += f"**Username:** @{username}\n"
    response += f"**User ID:** `{user.id}`\n"
    if is_group_context and chat:
        chat_id = getattr(chat, 'id', None)
        if chat_id:
            response += f"**Chat ID:** `{chat_id}`\n"
    if not is_bot:
        response += f"**Premium User:** {'Yes' if is_premium else 'No'}\n"
    response += f"**Data Center:** {dc_location}\n"
    if not is_bot:
        response += (
            f"**Created On:** {account_created_str}\n"
            f"**Account Age:** {account_age}\n"
        )
    restricted = getattr(user, 'restricted', False)
    response += f"**Account Frozen:** {'Yes' if restricted else 'No'}\n"
    if not is_bot:
        status_display = get_status_display(getattr(user, 'status', None))
        response += f"**Last Seen:** {status_display}\n"
    if getattr(user, 'support', False):
        response += "**Telegram Staff:** Yes\n"
    response += (
        f"**Permanent Link:** [Click Here](tg://user?id={user.id})\n"
        "━━━━━━━━━━━━━━━━\n"
        "**👁 Thank You for Using Our Tool ✅**"
    )
    return response, full_name


def format_chat_response(chat):
    dc_id = getattr(chat.photo, 'dc_id', 0) if chat.photo else 0
    dc_location = get_dc_location(dc_id)

    if isinstance(chat, Channel):
        if getattr(chat, 'megagroup', False):
            chat_type = "Supergroup"
        elif getattr(chat, 'broadcast', False):
            chat_type = "Channel"
        else:
            chat_type = "Group"
    elif isinstance(chat, Chat):
        chat_type = "Group"
    else:
        chat_type = "Unknown"

    full_name = getattr(chat, 'title', 'Unnamed Chat')
    members_count = getattr(chat, 'participants_count', 'Unknown')

    response = (
        f"**🔍 Showing {chat_type}'s Profile Info 📋**\n"
        "━━━━━━━━━━━━━━━━\n"
        f"**Full Name:** {full_name}\n"
    )
    username = getattr(chat, 'username', None)
    if username:
        response += f"**Username:** @{username}\n"

    chat_id = chat.id
    if isinstance(chat, Channel):
        display_id = int(f"-100{chat.id}")
    else:
        display_id = -chat.id if chat.id > 0 else chat.id

    response += (
        f"**Chat ID:** `{display_id}`\n"
        f"**Total Members:** {members_count}\n"
    )
    if username:
        response += f"**Permanent Link:** [Click Here](tg://resolve?domain={username})\n"
    response += (
        "━━━━━━━━━━━━━━━━\n"
        "**👁 Thank You for Using Our Tool ✅**"
    )
    return response, full_name
