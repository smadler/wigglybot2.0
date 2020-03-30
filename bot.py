# Work with Python 3.6
import discord
import os
import asyncio
import traceback
from discord.ext import commands

bot = commands.Bot(command_prefix=(('%', '$')), description='Wiggly Bot')
  
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    await bot.process_commands(message)
        

#tells me the bot is open and loads cogs
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    cogs = ['cogs.pokemon', 'cogs.pinmanager', 'cogs.wander']
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Couldn\'t load cog {cog}')
            traceback.print_exc()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run(str(os.environ.get('TOKEN'))))
