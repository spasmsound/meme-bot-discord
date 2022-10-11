import json
import logging
import os
import sys

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

            os.remove(message_dict['filename'])
        else:
            logger.error('File does not exists: ' + message_dict['filename'])

    if 'text' == message_dict['type']:
        await channel.send(message_dict['content'])

    quit()


discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))
