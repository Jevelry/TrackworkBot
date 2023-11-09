import discord
import trackworkChecker
from discord.ext import tasks
from pytz import timezone
import config
from datetime import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    getNewTrackWork.start()
 
@tasks.loop(hours=24)
async def getNewTrackWork():
    NorthShoreMessages = trackworkChecker.getNewTrackWork()
    MetroMessaage = trackworkChecker.getNewMetroTrackWork()
    now = datetime.now(timezone('Australia/Sydney'))
    await client.get_channel(1076339832093159527).send(f'Checked on {now.date()}')
    # Using Channel id for my server
    if NorthShoreMessages:
        for message in NorthShoreMessages:
            await client.get_channel(1076339832093159527).send(f'@here {message}')
    if MetroMessaage:
        await client.get_channel(1076339832093159527).send(f'@here {MetroMessaage}')

client.run(f'{config.bot_token}')

