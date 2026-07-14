"""
Telegram Listener - Monitors messages from "Task Officer", extracts
Google Maps links, and sends a notification via a bot.
"""

import asyncio
import os
import re
import sys

from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# ---------------------------------------------------------------------------
# Load environment variables from .env file
# ---------------------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")
SESSION_STRING = os.getenv("SESSION_STRING")

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
TARGET_SENDER_NAME = "Task Officer"  # Filter by sender display name
TARGET_CHAT_ID = None                # e.g. -1001234567890 (None = any chat)

# Messages containing any of these phrases will be ignored
SKIP_PHRASES = [
    "المهمة الجاية هتتنشر في الجروب قريب جدًا",
    "فيه 21 مهمة كل يوم",
    "لتأكيد Task",
    "اختار/ي المبلغ اللي مفضّل/اه للمهمة",
    "اللي لسه ما كمّلش WELFARE TASK",
    "مبروك للطلبة اللي كمّلوا",
    "تم نشر Task في الجروب",
    "كل Task بتاخد",
    "كمّل كل المهام عشان تنضم",
    "من فضلك تابع/ي مع الريسبشن وكمّل/ي WELFARE TASK",
    "تواصل/ي مع الريسبشن عشان السحب",
    "كمّل/ي المهمة وابعت/ي سكرينشوت إنجاز المهمة للريسبشن",
    "إحنا بننشر Task كل 25 دقيقة",
]

# ---------------------------------------------------------------------------
# Validate credentials
# ---------------------------------------------------------------------------
if not API_ID or not API_HASH:
    print("❌ Error: API_ID and API_HASH must be set in the .env file.")
    sys.exit(1)

if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN must be set in the .env file.")
    sys.exit(1)

if not SESSION_STRING:
    print("❌ Error: SESSION_STRING must be set in the .env file.")
    print("   Run: python generate_session.py")
    sys.exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    print("❌ Error: API_ID must be a number.")
    sys.exit(1)

if MY_CHAT_ID:
    MY_CHAT_ID = int(MY_CHAT_ID)
else:
    print("❌ Error: MY_CHAT_ID must be set in the .env file.")
    sys.exit(1)


async def handle_new_message(event):
    """Handle incoming messages - forward Task Officer's messages via bot."""
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()

        chat_name = getattr(chat, "title", None) or getattr(chat, "first_name", "Unknown")
        sender_name = (
            f"{getattr(sender, 'first_name', '') or ''} {getattr(sender, 'last_name', '') or ''}".strip()
            or "Unknown"
        )
        chat_id = event.chat_id
        message_text = event.raw_text

        # Only process messages from "Task Officer" (case-insensitive)
        if sender_name.lower() != TARGET_SENDER_NAME.lower():
            return

        # Skip messages that contain known irrelevant phrases
        if any(phrase in message_text for phrase in SKIP_PHRASES):
            return

        # If a specific chat is configured, filter by it
        if TARGET_CHAT_ID is not None and chat_id != TARGET_CHAT_ID:
            return

        # Build the notification message
        notification = (
            f"🚨 **New Task**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📌 Group: {chat_name}\n"
            f"👤 Sender: {sender_name}\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"{message_text}"
        )

        # Extract Google Maps links from the message
        urls = re.findall(r'https?://(?:maps\.app\.goo\.gl|(?:www\.)?google\.\w+/maps)\S+', message_text)

        if urls:
            # Send with clickable buttons - nice layout
            buttons = [
                [Button.url("📍 Open in Google Maps", urls[0])],
                [Button.url("⭐ Write a Review", urls[0])],
            ]
            await bot.send_message(MY_CHAT_ID, notification, buttons=buttons)
        else:
            await bot.send_message(MY_CHAT_ID, notification)

        print(f"✅ Notification sent! Message from {sender_name} in {chat_name}")

    except Exception as e:
        print(f"⚠️  Error processing message: {e}")


async def main():
    """Start both the user client (listener) and bot client (notifier)."""
    global bot

    # User client - uses string session (no interactive login needed)
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    # Bot client - sends notifications
    bot = TelegramClient(StringSession(), API_ID, API_HASH)

    # Register the message handler
    client.on(events.NewMessage)(handle_new_message)

    # Start both clients
    await client.start()
    await bot.start(bot_token=BOT_TOKEN)

    print("=" * 60)
    print("✅ Telegram Listener is running!")
    print(f"🎯 Listening for messages from: {TARGET_SENDER_NAME}")
    print(f"🔔 Notifications sent to chat ID: {MY_CHAT_ID}")
    print("=" * 60)

    # Keep running forever
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped by user.")
