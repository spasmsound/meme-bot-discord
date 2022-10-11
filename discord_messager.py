import json
import logging
import os
import sys
import shutil

import discord

intents = discord.Intents.default()
intents.message_content = True

discord_client = discord.Client(intents=intents)

message = sys.argv[1]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)


@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))
    print('Awaiting Telegram Message')

    # My channels are for RTX card drops and PS5
    channel = discord_client.get_channel(int(os.getenv('DISCORD_CHANNEL')))
    message_dict = json.loads(message)

    if 'image' == message_dict['type']:
        if os.path.exists(message_dict['filename']):
            await channel.send(file=discord.File(message_dict['filename']))
        else:
            logger.error('File does not exists: ' + message_dict['filename'])

    if 'text' == message_dict['type']:
        await channel.send(message_dict['content'])

    clean_temp_directory()

    quit()


def clean_temp_directory():
    folder = './temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))
