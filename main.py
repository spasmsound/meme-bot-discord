import json
import logging
import os
import subprocess
import sys
from datetime import datetime

from PIL import Image
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

if not os.path.exists('./temp'):
    os.makedirs('./temp')


def start():
    client = TelegramClient(os.getenv('SESSION_NAME'),
                            int(os.getenv('API_ID')),
                            os.getenv('API_HASH'))
    client.start()

    input_channels_entities = []

    for d in client.iter_dialogs():
        if d.entity.id == int(os.getenv('TELEGRAM_CHANNEL_ID')):
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
            break

    if not input_channels_entities:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(input_channels_entities)} channels.")

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        if event.media is None:
            message = {'type': 'text', 'content': event.message.message}
        else:
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            full_filename = './temp/' + str(ts) + '.jpg'

            await client.download_media(event.message, full_filename)

            img_valid = False
            try:
                img = Image.open(full_filename)
                img.verify()

                img_valid = True
            except Exception:
                pass

            if not img_valid:
                return

            message = {'type': 'image', 'filename': full_filename}

        string_message = json.dumps(message)
        subprocess.call(["python3", "discord_messager.py", string_message])

    client.run_until_disconnected()


if __name__ == "__main__":
    start()
