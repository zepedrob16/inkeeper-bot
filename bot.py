import os
import random
import discord
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='ttb', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx, *game_full_name):

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

   # response = (
    #        f'**Main Story**: {best_element.gameplay_main} hours \n'
    #        f'**Main + Extra**: {best_element.gameplay_main_extra} hours \n'
   #         f'**Completionist**: {best_element.gameplay_completionist} hours \n'
   #     )

    #await message.channel.send(embed=embed)

    await ctx.send(embed=embed)

bot.run(TOKEN)