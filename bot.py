import os
import random
import discord
import requests
import omdb
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_KEY = os.getenv('API_KEY')

omdb.set_default('apikey', API_KEY)

bot = commands.Bot(command_prefix='!')

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

    else:
        await ctx.send('No results found')
        return

    embed = discord.Embed(
        title = best_element.game_name,
        description = best_element.game_web_link,
        colour = discord.Colour.blue()
    )

    embed.set_footer(text=":)")
    embed.set_image(url = best_element.game_image_url)

    if best_element.gameplay_main != -1:
        embed.add_field(name = "Main Story", value = best_element.gameplay_main + "hours", inline = True)

    if best_element.gameplay_main_extra != -1:
        embed.add_field(name = "Main + Extra", value = best_element.gameplay_main_extra + "hours", inline = True)

    if best_element.gameplay_completionist != -1:
        embed.add_field(name = "Completionist", value = best_element.gameplay_completionist + "hours", inline = True)

    await ctx.send(embed=embed)

@bot.command(name='movie', help='Responds with information obtained from metacritic')
async def imdb(ctx, *movie_full_name):
    movie = ''

    if len(movie_full_name) > 1:
        for element in movie_full_name:
            movie = movie + element + ' '
    
    else:
        movie = movie_full_name[0]

    info = omdb.search_movie(movie_full_name)

    if len(info) > 0:
        info = omdb.imdbid(info[0]['imdb_id'])
    
    else:
        await ctx.send('No results found')
        return

    embed = discord.Embed(
        title = info['title'],
        description = info['plot'],
        colour = discord.Colour.blue()
    )

    embed.set_footer(text = 'A ' + info['production'] + ' production')
    embed.set_image(url = info['poster'])
    embed.add_field(name = "Release Date", value = info['released'], inline = False)
    embed.add_field(name = "Director(s)", value = info['director'], inline = False)
    embed.add_field(name = "MetaScore", value = info['metascore'], inline = True)
    embed.add_field(name = "IMDB Score", value = info['imdb_rating'], inline = True)

    await ctx.send(embed=embed)

bot.run(TOKEN)