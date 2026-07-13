"""
Run this script ONCE locally to generate a string session.
Copy the output string and paste it into your .env file as SESSION_STRING.
"""

import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


async def main():
    # Create a client with StringSession to get a portable session string
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.start()

    # Print the session string
    session_string = client.session.save()
    print("\n" + "=" * 60)
    print("✅ Your session string (copy this into .env as SESSION_STRING):")
    print("=" * 60)
    print(session_string)
    print("=" * 60)
    print("\n⚠️  Keep this secret! Anyone with it can access your account.")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
