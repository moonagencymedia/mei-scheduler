import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
STRING_SESSION = os.environ["TELEGRAM_STRING_SESSION"]
CHANNEL_ID = int(os.environ["TELEGRAM_CHANNEL_ID"])

async def send_post(post):
    async with TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH) as client:
        caption = post.get("caption", "")
        image_path = post.get("image", None)
        if image_path and os.path.exists(image_path):
            await client.send_file(CHANNEL_ID, image_path, caption=caption)
            print(f"✅ Post avec image envoyé")
        else:
            await client.send_message(CHANNEL_ID, caption)
            print(f"✅ Post texte envoyé")

async def main():
    schedule_file = "posts/schedule.json"
    if not os.path.exists(schedule_file):
        print("❌ Fichier schedule.json introuvable")
        sys.exit(1)
    with open(schedule_file, "r", encoding="utf-8") as f:
        schedule = json.load(f)
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    current_hour = now.hour
    print(f"📅 Date : {today} | Heure UTC : {current_hour}h")
    posts_today = schedule.get(today, [])
    if not posts_today:
        print(f"ℹ️ Aucun post prévu pour aujourd'hui")
        return
    for post in posts_today:
        post_hour = post.get("hour_utc")
        if abs(post_hour - current_hour) <= 1:
            print(f"📤 Envoi du post prévu à {post_hour}h UTC...")
            await send_post(post)
            return
    print(f"ℹ️ Aucun post à envoyer à {current_hour}h UTC")

if __name__ == "__main__":
    asyncio.run(main())
