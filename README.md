# Telegram Listener

A simple Python application that monitors messages from a specific Telegram group and sender, then automatically forwards matching messages to your Saved Messages.

## Prerequisites

- Python 3.8 or higher
- A Telegram account
- API credentials from Telegram

## Setup

### 1. Get Telegram API Credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click on **API development tools**
4. Create a new application (fill in any name/description)
5. Note down your **API ID** and **API Hash**

### 2. Install Dependencies

```bash
cd telegram-listener
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit the `.env` file and replace the placeholder values:

```env
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
```

### 4. First Run (Discovery Mode)

Run the script with the default configuration:

```bash
python main.py
```

On the first run, Telethon will ask for:
- Your **phone number** (international format, e.g. `+1234567890`)
- The **login code** sent to your Telegram app
- Your **2FA password** (if enabled)

After login, a `session.session` file is created so you won't need to log in again.

With `TARGET_CHAT_ID` and `TARGET_SENDER_ID` set to `None`, the script prints details for every incoming message:

```
============================================================
📨 New Message (Discovery Mode)
   Chat Name : My Group
   Chat ID   : -1001234567890
   Sender    : John Doe
   Sender ID : 123456789
   Message   : Hello everyone!
============================================================
```

### 5. Configure Filtering

Once you've identified the Chat ID and Sender ID you want to monitor, edit `main.py` and set:

```python
TARGET_CHAT_ID = -1001234567890    # Your target group's ID
TARGET_SENDER_ID = 123456789        # The sender's ID
```

### 6. Run in Filtered Mode

```bash
python main.py
```

Now the script will only react to messages from the configured sender in the configured group, and forward them to your Saved Messages in this format:

```
🚨 New Task
Group: My Group
Sender: John Doe

Message:
<original message text>
```

## Project Structure

```
telegram-listener/
├── .env                # API credentials (do NOT commit this)
├── main.py             # Main application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── session.session     # Auto-generated session file (do NOT commit)
```

## Notes

- **Session file**: The `session.session` file stores your login session. Keep it private — anyone with this file can access your Telegram account.
- **Security**: Never commit `.env` or `session.session` to version control. Add them to `.gitignore`.
- **Stopping**: Press `Ctrl+C` to stop the listener gracefully.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `API_ID must be a number` | Make sure API_ID in `.env` is just the number, no quotes |
| `AuthKeyError` or session issues | Delete `session.session` and log in again |
| No messages appearing | Make sure you're receiving messages in the Telegram app first |
| `FloodWaitError` | Telegram rate limit — wait the indicated time and retry |
