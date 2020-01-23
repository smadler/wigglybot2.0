import discord
from discord import File
from discord.ext import commands

class Matchup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    types_dict={}
    with open("types2.txt", 'r') as f:
        for line in f:
            items = line.split('%')
            key, values = items[0], items[1:]
            types_dict[key] = values

    @commands.command()
    async def matchup(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            msg = ('Invalid input!')

        else:
            msg=""
            mt=""
            if arg2==None:
                #no 2nd argument
                types=arg1.split("/")
                if len(types)==1:
                    ptype =str(types[0].capitalize())
                    ptype+="/"+str(types[0].capitalize())
                    mt=str(types[0])
                else:
                    ptype = str(types[0].capitalize())
                    ptype+="/"+str(types[1].capitalize())
            else:
                ptype = str(arg1.capitalize())
                ptype+="/"+str(arg2.capitalize())

            if (ptype not in self.types_dict):
                msg += "Invalid input!"

            else:
                t=ptype.split("/")
                if(t[0])==t[1]):
                    msg+=' For ' + mt +' types, use '
                else:
                    msg+=' For ' + str(ptype) +' types, use '
                msg+='\n'.join(map(str, self.types_dict.get(ptype))).rstrip()
                msg+=' type moves!'

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Matchup(bot))
