import os

import discord
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    results = HowLongToBeat().search("Nioh")

    if results is not None and len(results) > 0:
        best_element = max(results, key=lambda element: element.similarity)

    print (
        f'Main Story {best_element.gameplay_main} \n'
        f'Main + Extra {best_element.gameplay_main_extra} \n'
        f'Completionist {best_element.gameplay_completionist} \n'
    )

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} has connected to Discord!'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)