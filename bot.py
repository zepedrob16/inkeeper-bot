import os
import random
import discord
import requests
import json
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

metacritic_url = "https://chicken-coop.p.rapidapi.com/games"
headers = {
    'x-rapidapi-host': "chicken-coop.p.rapidapi.com",
    'x-rapidapi-key': "e1d46b5a6cmsh435ae7b9b898362p193c22jsn03fc6e995827"
}

@bot.command(name='ttb', help='Responds with information obtained from howlongtobeat')
async def howlongtobeat(ctx, *game_full_name):
    game = ''
    
    if len(game_full_name) > 1:
        for element in game_full_name:
            game = game + element + ' '
    
    else:
        game = game_full_name[0]

    results = HowLongToBeat().search(game)

    if results is not None and len(results) > 0:
        best_element = max(results, key=lambda element: element.similarity)

    embed = discord.Embed(
        title = best_element.game_name,
        description = best_element.game_web_link,
        colour = discord.Colour.blue()
    )

    embed.set_footer(text=":)")
    embed.set_image(url = best_element.game_image_url)
    embed.add_field(name = "Main Story", value = best_element.gameplay_main + "hours", inline = True)
    embed.add_field(name = "Main + Extra", value = best_element.gameplay_main_extra + "hours", inline = True)
    embed.add_field(name = "Completionist", value = best_element.gameplay_completionist + "hours", inline = True)

    await ctx.send(embed=embed)

@bot.command(name='meta', help='Responds with information obtained from metacritic')
async def metacritic(ctx, *game_full_name):
    game = ''
    
    if len(game_full_name) > 1:
        for element in game_full_name:
            game = game + element + ' '
    
    else:
        game = game_full_name[0]

    querystring = {"title": game}

    response = requests.request("GET", metacritic_url, headers=headers, params=querystring)

    results = json.loads(response.text)["result"]
    
    if results is not None and len(results) > 0:
        best_element = results[0]

    print(best_element)


bot.run(TOKEN)