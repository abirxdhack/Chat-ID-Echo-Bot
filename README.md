# QuickInfoBot
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)
![Telethon](https://img.shields.io/badge/Telethon-Latest-orange)

A fast and feature-rich Telegram bot to instantly fetch detailed info and IDs for users, bots, groups, and channels.

Maintained by [abirxdhack](https://github.com/abirxdhack) • [Repository](https://github.com/abirxdhack/Chat-ID-Echo-Bot)

---

## ✨ Features

- **Shared Peer Info** — Share any user, bot, group, or channel via keyboard buttons and get full details with profile photo instantly
- **Forwarded Message Info** — Forward any message to extract the sender's ID, name, and photo
- **Username Lookup** — Send `@username` directly to get profile info
- **Inline Mode** — Use `@BotUsername query` in any chat to look up entities inline
- **Link Generator** — Get Android/iOS deep links and join links for any entity
- **Admin & Owner Chat Finder** — Dedicated buttons to share chats where you're an admin or owner
- **Profile Photos** — Fetched directly from the shared peer object, no extra API calls
- **Non-blocking Handlers** — All heavy operations run as async tasks via `@new_task`
- **Smart Buttons** — All keyboards built with the `SmartButtons` class for clean and consistent UI
- **Flood & Error Handling** — All network calls wrapped with FloodWait, blocked user, and general error handling

---

## 📋 Prerequisites

- Python 3.9+
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` from [BotFather](https://t.me/BotFather)

---

## 🛠 Installation

```bash
git clone https://github.com/abirxdhack/Chat-ID-Echo-Bot.git
cd Chat-ID-Echo-Bot
pip install telethon python-dateutil
```

Edit `config.py` with your credentials:

```python
API_ID    = "your_api_id"
API_HASH  = "your_api_hash"
BOT_TOKEN = "your_bot_token"
ADMIN_ID  = 123456789
```

---

## 🚀 Usage

```bash
python3 main.py
```

Then in Telegram:

| Action | Result |
|---|---|
| `/start` | Welcome message with sharing keyboard |
| `/me` | Your own profile info |
| `/info @username` | Profile info for any entity |
| `/link @username` | Deep links for any entity |
| `/admin` | Share a chat where you're an admin |
| `/my` | Share a chat you own |
| `/help` | Full feature guide |
| Send `@username` | Instant username lookup |
| Forward a message | Extract sender info |
| Inline `@bot query` | Inline entity lookup in any chat |

---

## 📁 Project Structure

```
QuickInfoBot/
├── main.py               # Entry point
├── bot.py                # Telethon client
├── config.py             # Credentials and settings
├── core/
│   └── start.py          # /start command
├── modules/
│   ├── admin.py          # /admin command
│   ├── callback.py       # Reply keyboard button handlers
│   ├── fwd.py            # Forwarded message handler
│   ├── help.py           # /help command
│   ├── info.py           # /info and /id commands
│   ├── inline.py         # Inline query handler
│   ├── link.py           # /link command
│   ├── me.py             # /me command
│   ├── my.py             # /my command
│   └── username.py       # @username handler
├── shared/
│   └── chatinfo.py       # Shared peer handler
├── miscs/
│   ├── startbtn.py       # Main menu keyboard
│   ├── adbtn.py          # Admin keyboard
│   └── mybtn.py          # Owner keyboard
└── utils/
    ├── logger.py          # Logging setup
    ├── decorators.py      # @new_task, clean_download
    ├── buttons.py         # SmartButtons class
    ├── helpers.py         # Formatters, DC info, account age
    └── functions.py       # send_message, edit_message, etc.
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push and open a pull request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 📧 Contact

[abirxdhack](https://github.com/abirxdhack) • Telegram: [@TheSmartDev](https://t.me/TheSmartDev)