# Work with Python 3.6
import discord
import os
import asyncio
import traceback
from discord.ext import commands

bot = commands.Bot(command_prefix=(('%', '$')), description='Wiggly Bot')

#tells me the bot is open and loads cogs
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    cogs = ['cogs.pokemon', 'cogs.pinmanager', 'cogs.denimager', 'cogs.cramomatic', 'cogs.wiki']
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Couldn\'t load cog {cog}')
            traceback.print_exc()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run(str(os.environ.get('TOKEN'))))
