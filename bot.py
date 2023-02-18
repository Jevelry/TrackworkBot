import discord
import trackworkChecker
from discord.ext import tasks
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
    NorthShoreMessage = trackworkChecker.getNewTrackWork()
    MetroMessaage = trackworkChecker.getNewMetroTrackWork()
    await client.get_channel(1076339832093159527).send(f'Checked at {datetime.now()}')
    # Using Channel id for my server
    if NorthShoreMessage:
        await client.get_channel(1076339832093159527).send(f'@everyone {NorthShoreMessage}')
    if MetroMessaage:
        await client.get_channel(1076339832093159527).send(f'@everyone {MetroMessaage}')

client.run(f'{config.bot_token}')

