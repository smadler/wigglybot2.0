import discord
from discord import File
from discord.ext import commands

class Matchup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    types_dict={}
        with open("types.txt", 'r') as f:
          for line in f:
            items = line.split('/')
            key, values = items[0], items[1:]
            types_dict[key] = values

    @commands.command()
    async def matchup(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            msg = ('Invalid input!')

        elif arg1 != None and arg2 == None:
            ptype = arg1.capitalize()

            if ptype not in self.types_dict:
                msg = "Invalid input!"

            else:
                ptypeval=''.join(map(str,self.types_dict.get(ptype)))
                msg='For ' + str(search) + ' types, use '+ ptypeval.rstrip() + ' type moves!'

        elif arg2!=None:
            msg="Currently only supports searching for one type!"

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Matchup(bot))
